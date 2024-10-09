import sys
import os
import logging
import re
from datetime import datetime
import moviepy.editor as mp
import whisper
from transformers import pipeline, BertForTokenClassification, BertTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from pathlib import Path
import json
import warnings
from transformers import logging as hf_logging
import subprocess
import shutil
import pysrt

# Supressão de avisos da biblioteca transformers
hf_logging.set_verbosity_error()
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

def load_config():
    """Carrega as configurações do arquivo JSON."""
    with open('config.json', 'r') as f:
        return json.load(f)

# Carregar as configurações
config = load_config()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Diretórios
SUBTITLE_DIR = BASE_DIR / config['directories']['subtitles']
CLIPS_DIR = BASE_DIR / config['directories']['clips']
LOGS_DIR = BASE_DIR / config['directories']['logs']['dir']
VIDEOS_DIR = BASE_DIR / config['directories']['videos']
AUDIO_DIR = BASE_DIR / config['directories']['audio']

# Parametros
num_topics = config['video_processing']['num_topics']
num_keywords = config['video_processing']['num_keywords']
min_duration = config['video_processing']['min_duration']
max_duration = config['video_processing']['max_duration']
max_words_per_segment = config['max_words_per_segment']
font_file = config['font_file']

# Carregar o modelo Whisper do config.json
whisper_model = whisper.load_model(config['whisper_model'])

# Carregar o score minimo no sentimento do config.json
min_sent_score = config['video_processing']['min_sentiment_score']

def ensure_directories_exist():
    """Garante que as pastas necessárias existam antes de configurar o logging."""
    directories = [SUBTITLE_DIR, CLIPS_DIR, LOGS_DIR, VIDEOS_DIR, AUDIO_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

ensure_directories_exist()

# Configuração do logging
log_filename = LOGS_DIR / config['directories']['logs']['archive']
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializa os pipelines com base nas configurações
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ['TEMP'] = str(AUDIO_DIR)
os.environ['TMPDIR'] = str(AUDIO_DIR)
os.environ['TMP'] = str(AUDIO_DIR)
sentiment_analyzer = pipeline("sentiment-analysis", model=config['sentiment_model'])
emotion_analyzer = pipeline("text-classification", model=config['emotion_model'])

# Carrega o modelo de NER
ner_model = BertForTokenClassification.from_pretrained(
    config['ner_model'],
    ignore_mismatched_sizes=True
)

# Carrega o tokenizer correspondente ao modelo NER
ner_tokenizer = BertTokenizer.from_pretrained(config['ner_model'])

# Inicializa o pipeline de NER
ner_analyzer = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")

def clean_text(text):
    """Remove caracteres especiais e limpa o texto.""" 
    return re.sub(r'\s+', ' ', text).strip()

def extract_audio(video_path, audio_output_path):
    """Extrai o áudio de um vídeo e salva em um arquivo temporário na pasta de áudio."""  
    logging.info(f"Extraindo áudio do vídeo: {video_path}")
    try:
        video = mp.VideoFileClip(str(video_path))
        audio = video.audio
        
        # Especificar o caminho de saída para o arquivo de áudio
        audio.write_audiofile(str(audio_output_path), codec='mp3')  # Salvar na pasta de áudio
        logging.info(f"Áudio extraído e salvo em: {audio_output_path}")
    except Exception as e:
        logging.error(f"Erro ao extrair áudio: {e}")
        raise


def transcribe_audio(audio_path):
    """Transcreve o áudio utilizando o modelo Whisper."""    
    logging.info(f"Iniciando a transcrição do áudio: {audio_path}")
    try:
        result = whisper_model.transcribe(audio_path, verbose=True)
        logging.info("Transcrição concluída com sucesso")
        return result["segments"]
    except Exception as e:
        logging.error(f"Erro ao transcrever o áudio: {e}")
        raise

def format_time(seconds):
    """Converte tempo em segundos para o formato SRT (HH:MM:SS,mmm)."""
    millisec = int((seconds - int(seconds)) * 1000)
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

def generate_unique_id():
    """Gera um ID único baseado no timestamp."""    
    return datetime.now().strftime("%Y%m%d%H%M%S")
    
def save_subtitles(segments, output_dir, unique_id, video_name):
    """Salva os segmentos transcritos como arquivos SRT na pasta subtitles."""
    subtitles_subfolder = output_dir / f"{video_name}_{unique_id}"
    subtitles_subfolder.mkdir(parents=True, exist_ok=True)

    logging.info(f"Salvando legendas em: {subtitles_subfolder}")

    for i, segment in enumerate(segments):
        subtitle_filename = f"{video_name}_{unique_id}_{i + 1}.srt"
        subtitle_path = subtitles_subfolder / subtitle_filename

        logging.info(f"Salvando a transcrição como legenda em: {subtitle_path}")

        try:
            with open(subtitle_path, 'w', encoding='utf-8') as f:
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                text = segment['text']

                f.write(f"1\n")  # ID do segmento
                f.write(f"{start_time} --> {end_time}\n") 
                f.write(f"{text.strip()}\n")  # Texto

            logging.info(f"Legenda salva com sucesso em: {subtitle_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar a legenda: {e}")
            raise

    return subtitles_subfolder 

def analyze_sentiment(text: str):
    """Analisa o sentimento de um texto e retorna o rótulo e o score."""    
    result = sentiment_analyzer(text)[0]
    # logging.info(f"Análise de sentimento: Texto: '{text}' | Rótulo: {result['label']} | Score: {result['score']}")
    return result['label'], result['score']

def extract_topics(segments, num_topics=num_topics, num_keywords=num_keywords):
    text_data = [segment['text'] for segment in segments if segment['text'].strip()]
    num_documents = len(text_data)

    if num_documents < 2:
        raise ValueError("O número de segmentos é muito pequeno para extrair tópicos.")

    try:
        vectorizer = CountVectorizer(max_df=0.95, min_df=1, stop_words='english')
        doc_term_matrix = vectorizer.fit_transform(text_data)

        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(doc_term_matrix)

        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_keywords = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-num_keywords - 1:-1]]
            topics.append(top_keywords)

        return topics

    except ValueError as e:
        logging.error(f"Erro ao ajustar o vectorizer: {str(e)}")
        return []

def select_best_segments(segments: list, min_sentiment_score: float, min_duration: int = min_duration, max_duration: int = max_duration) -> list:
    """Seleciona todos os segmentos com base na análise de sentimentos e duração, sem limite de quantidade."""
    selected_segments = []
    sentiment_summary = {'positive': 0, 'negative': 0, 'neutral': 0}

    # Extrair tópicos para todos os segmentos
    topics = extract_topics(segments)
    segment_motives = []
    for segment in segments:
        text = clean_text(segment['text'])
        label, score = analyze_sentiment(text)

        motivo = ""
        if score >= min_sentiment_score:
            if score > 0.9:
                motivo = "Sentimento extremamente positivo ou negativo"
            elif 0.7 <= score <= 0.9:
                motivo = "Sentimento moderado com relevância"
            else:
                motivo = "Pontuação de sentimento aceitável, alinhado com o contexto"

            segment['sentiment'] = label
            segment['sentiment_score'] = score
            segment['topics'] = topics
            selected_segments.append(segment)

            segment_motives.append({
                'texto': text[:30], 
                'sentimento': label,
                'score': score,
                'motivo': motivo
            })

            sentiment_summary[label] = sentiment_summary.get(label, 0) + 1

    logging.info(f"{len(selected_segments)} segmentos selecionados.")
    logging.info(f"Resumo de sentimentos: {sentiment_summary}")
    logging.info(f"Estilo predominante do vídeo: {max(sentiment_summary, key=sentiment_summary.get)}")
    logging.info("Motivos para seleção dos segmentos:")

    # Combine os segmentos selecionados
    combined_segments = combine_segments(selected_segments, min_duration, max_duration)

    # Retorne apenas os segmentos que atendem ao critério de pontuação
    ranked_segments = [seg for seg in combined_segments if seg['sentiment_score'] >= min_sentiment_score]

    logging.info(f"Segmentos combinados finalizados: {len(ranked_segments)} selecionados.")

    return ranked_segments

def combine_segments(selected_segments, min_duration, max_duration):
    """Combina segmentos adjacentes em cortes válidos, sem limitar a quantidade de segmentos."""    
    combined_segments = []
    current_segment = []
    current_duration = 0
    current_start_time = 0

    for segment in selected_segments:
        segment_duration = segment['end'] - segment['start']

        if current_duration + segment_duration <= max_duration:
            if not current_segment:
                current_start_time = segment['start']
            current_segment.append(segment)
            current_duration += segment_duration
        else:
            if current_duration >= min_duration:
                combined_segments.append(create_combined_segment(current_segment, current_start_time))
                logging.info(f"Combinando segmentos: {[seg['text'] for seg in current_segment]} | Duração total: {current_duration}")
            current_segment = [segment]
            current_duration = segment_duration
            current_start_time = segment['start']

    if current_duration >= min_duration:
        combined_segments.append(create_combined_segment(current_segment, current_start_time))
        logging.info(f"Combinando segmentos: {[seg['text'] for seg in current_segment]} | Duração total: {current_duration}")

    return combined_segments  # Sem limitação de número de segmentos

def create_combined_segment(segments, start_time):
    """Cria um segmento combinado de vários segmentos menores."""
    combined_text = " ".join([segment['text'] for segment in segments])
    end_time = segments[-1]['end']

    return {
        'start': start_time,
        'end': end_time,
        'text': combined_text,
        'sentiment_score': segments[-1]['sentiment_score']
    }

def add_subtitle(clip_path, srt_filename, font_size=20, 
                 font_color="16777215", border_color="0", border_width=4,
                 alignment=2, width=480, 
                          height=720, x=400, y=0):  # Ajuste aqui
    srt_temp_file = None  # Inicializa como None para garantir que exista
    try:
        # Verificar se os parâmetros não são None
        if not font_file:
            logging.error("Parâmetros inválidos. font_file não podem ser None.")
            logging.warning("Alterando fonte padrão para Arial.")
            font_file = 'Arial'
        
        # Verificar se o arquivo SRT e o vídeo existem
        if not os.path.exists(srt_filename):
            raise FileNotFoundError(f"Arquivo SRT não encontrado: {srt_filename}")
        
        if not os.path.exists(clip_path):
            raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {clip_path}")
        
        subs = pysrt.open(srt_filename)
        srt_temp_file = 'temp_subtitles.srt'
        with open(srt_temp_file, 'w', encoding='utf-8') as f:
            for sub in subs:
                f.write(f"{sub.index}\n")
                start_time = f"{sub.start.hours:02}:{sub.start.minutes:02}:{sub.start.seconds:02},{sub.start.milliseconds:03}"
                end_time = f"{sub.end.hours:02}:{sub.end.minutes:02}:{sub.end.seconds:02},{sub.end.milliseconds:03}"
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{sub.text}\n\n")

        if clip_path is not None:
            temp_output_path = clip_path.replace('.mp4', '_temp.mp4')
        else:
            logging.error("O caminho do clipe é None.")
        temp_output_path = clip_path.replace('.mp4', '_temp.mp4')
        
        command = [
            'ffmpeg',
            # '-report', # log desse treco
            '-y', 
            '-i', clip_path,
            '-vf', (f"crop={width}:{height}:{x}:{y},"
                    f"subtitles={srt_temp_file}:"
                    f"force_style='FontName={font_file},"
                    f"FontSize={font_size},"
                    f"PrimaryColour={font_color},"
                    f"BorderStyle=1,"
                    f"Outline={border_width},"
                    f"OutlineColour={border_color},"
                    f"Alignment={alignment}'"
                ),
            '-codec:a', 'copy', 
            temp_output_path  
        ]
        
        subprocess.run(command, check=True)
        logging.info(f"Legenda adicionada com sucesso no vídeo '{clip_path}'. Arquivo de saída temporário: '{temp_output_path}'")
        
        shutil.move(temp_output_path, clip_path)
        logging.info(f"O arquivo temporário foi movido para substituir o original: {clip_path}")
        
    except ValueError as e:
        logging.error(f"Erro de valor: {e}")
    except FileNotFoundError as e:
        logging.error(e)
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao adicionar legenda: {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
    finally:
        if srt_temp_file and os.path.exists(srt_temp_file):
            os.remove(srt_temp_file)
            logging.info(f"Arquivo temporário {srt_temp_file} removido com sucesso.")

def save_clips(video_path, selected_segments, unique_id, video_name):
    """Salva os clipes selecionados em uma nova pasta, usando SRTs para nomeação e referência."""
    clip_subfolder = CLIPS_DIR / f"{video_name}_{unique_id}" 
    clip_subfolder.mkdir(parents=True, exist_ok=True)

    clips_saved = []

    for i, segment in enumerate(selected_segments):
        start_time = segment['start']
        end_time = segment['end']
        srt_filename = SUBTITLE_DIR / f"{video_name}_{unique_id}/{video_name}_{unique_id}_{i + 1}.srt"  # acho que n vai usar, guardar pq mudei pro processar_video
        clip_filename = f"{video_name}_{unique_id}_{i + 1}.mp4"  # Nome do clipe
        clip_path = clip_subfolder / clip_filename

        try:
            video = mp.VideoFileClip(str(video_path))
            clip = video.subclip(start_time, end_time)
            clip.write_videofile(str(clip_path), codec="libx264")
            clips_saved.append(clip_path)
            srt_filename = generate_srt_from_video(str(clip_path), srt_filename)
            add_subtitle(str(clip_path), srt_filename)
            logging.info(f"Clip salvo: {clip_path}")

        except Exception as e:
            logging.error(f"Erro ao salvar o clipe {clip_filename}: {e}")

    return clips_saved

def clean_up_audio_files():
    """Remove todos os arquivos de áudio após o término do processo, incluindo temporários."""
    logging.info("Removendo arquivos de áudio...")
    for audio_file in AUDIO_DIR.glob('*'):
        try:
            audio_file.unlink()
            logging.info(f"Arquivo de áudio removido: {audio_file}")
        except Exception as e:
            logging.error(f"Erro ao remover o arquivo de áudio {audio_file}: {e}")

def split_transcript_into_segments(segments):
    """Divide a transcrição em segmentos respeitando o tempo."""
    divided_segments = []
    
    for segment in segments:
        text = segment["text"].strip()
        words = text.split()
        start_time = segment["start"]
        end_time = segment["end"]
        for i in range(0, len(words), max_words_per_segment):
            chunk_words = words[i:i + max_words_per_segment]
            chunk_text = ' '.join(chunk_words)
            
            chunk_start = start_time + (i / len(words)) * (end_time - start_time)
            chunk_end = start_time + ((i + len(chunk_words)) / len(words)) * (end_time - start_time)
            
            divided_segments.append({
                "start": chunk_start,
                "end": chunk_end,
                "text": chunk_text
            })
    
    return divided_segments

# Geração do arquivo SRT
def generate_srt(segments, srt_output_path):
    """Gera um arquivo SRT a partir de uma lista de segmentos."""
    subs = pysrt.SubRipFile()
    
    for i, segment in enumerate(segments):
        start_time = pysrt.SubRipTime(seconds=segment['start'])
        end_time = pysrt.SubRipTime(seconds=segment['end'])
        text = segment['text']
        
        sub = pysrt.SubRipItem(index=i + 1, start=start_time, end=end_time, text=text)
        subs.append(sub)
    
    # Salva o arquivo SRT
    subs.save(srt_output_path, encoding='utf-8')
    logging.info(f"Arquivo SRT salvo em: {srt_output_path}")
    return srt_output_path

def generate_srt_from_video(video_path, srt_output_path):
    """Gera um arquivo SRT a partir de um vídeo."""
    if video_path is not None:
        audio_output_path = video_path.replace('.mp4', '.mp3')
    else:
        logging.error("O caminho do vídeo é None.")
    audio_output_path = video_path.replace('.mp4', '.mp3')
    extract_audio(video_path, audio_output_path)
    transcript_segments = transcribe_audio(audio_output_path)
    segments = split_transcript_into_segments(transcript_segments)
    srt_output_path = generate_srt(segments, srt_output_path)

    if os.path.exists(audio_output_path):
        os.remove(audio_output_path)

    return srt_output_path

def process_video(video_path):
    """Processa o vídeo completo, extraindo o áudio, transcrevendo, selecionando e salvando clipes."""  
    audio_output_path = AUDIO_DIR / f"{Path(video_path).stem}.mp3"
    unique_id = generate_unique_id()  # Gera um ID único
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    try:
        extract_audio(video_path, audio_output_path)
        segments = transcribe_audio(str(audio_output_path))
        selected_segments = select_best_segments(segments, min_sent_score)

        if selected_segments:
            save_subtitles(selected_segments, SUBTITLE_DIR, unique_id, video_name)
            clips_saved = save_clips(video_path, selected_segments, unique_id, video_name)
            
            # Log resumido e final
            logging.info(f"Processamento concluído: {len(selected_segments)} segmentos escolhidos, {len(clips_saved)} clipes salvos.")
    
    except Exception as e:
        logging.error(f"Erro no processamento do vídeo: {e}")
    finally:
        clean_up_audio_files()

if __name__ == "__main__":
    video_file_path = sys.argv[1]
    process_video(video_file_path)
