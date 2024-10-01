import sys
import os
import logging
import re
from datetime import datetime
import moviepy.editor as mp
import whisper
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from pathlib import Path
import json
import warnings
from transformers import logging as hf_logging

# Supressão de avisos da biblioteca transformers
hf_logging.set_verbosity_error()
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Diretórios
SUBTITLE_DIR = BASE_DIR / "subtitles"
CLIPS_DIR = BASE_DIR / "clips"
LOGS_DIR = BASE_DIR / "logs"
VIDEOS_DIR = BASE_DIR / "videos"
AUDIO_DIR = BASE_DIR / "audio"  # Diretório para o áudio extraído


def load_config():
    """Carrega as configurações do arquivo JSON."""
    with open('config.json', 'r') as f:
        return json.load(f)

# Carregar as configurações
config = load_config()

def ensure_directories_exist():
    """Garante que as pastas necessárias existam antes de configurar o logging."""
    directories = [SUBTITLE_DIR, CLIPS_DIR, LOGS_DIR, VIDEOS_DIR, AUDIO_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

ensure_directories_exist()

# Configuração do logging
log_filename = LOGS_DIR / "process.log"
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
from transformers import BertForTokenClassification, BertTokenizer

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


def transcribe_audio(audio_path, model):
    """Transcreve o áudio utilizando o modelo Whisper."""    
    logging.info(f"Iniciando a transcrição do áudio: {audio_path}")
    try:
        result = model.transcribe(str(audio_path), verbose=True)
        logging.info("Transcrição concluída com sucesso")
        return result["segments"]
    except Exception as e:
        logging.error(f"Erro ao transcrever o áudio: {e}")
        raise

def format_time(seconds):
    """Formata o tempo em segundos para o formato SRT."""    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def generate_unique_id():
    """Gera um ID único baseado no timestamp."""    
    return datetime.now().strftime("%Y%m%d%H%M%S")

def save_subtitles(segments, video_path, output_dir):
    """Salva os segmentos transcritos como um arquivo SRT na pasta subtitles."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    unique_id = generate_unique_id()  # ID único para o vídeo
    subtitle_filename = f"{video_name}_{unique_id}.srt"
    subtitle_path = output_dir / subtitle_filename

    logging.info(f"Salvando a transcrição como legenda em: {subtitle_path}")
    try:
        with open(subtitle_path, 'w') as f:
            for i, segment in enumerate(segments):
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                text = segment['text']
                duration = segment['end'] - segment['start']  # Cálculo da duração
                duration_formatted = format_time(duration)  # Formata a duração

                segment_id = f"{video_name}_{unique_id}_{i + 1}"  # ID único para o segmento

                f.write(f"{segment_id}\n")  # Escreve o ID do segmento
                f.write(f"{start_time} --> {end_time} (Duração: {duration_formatted})\n")  # Inclui a duração
                f.write(f"{text.strip()}\n\n")

        logging.info(f"Legenda salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda: {e}")
        raise

def analyze_sentiment(text: str):
    """Analisa o sentimento de um texto e retorna o rótulo e o score."""    
    result = sentiment_analyzer(text)[0]
    # logging.info(f"Análise de sentimento: Texto: '{text}' | Rótulo: {result['label']} | Score: {result['score']}")
    return result['label'], result['score']


def extract_topics(segments, num_topics=5, num_keywords=10):
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

def select_best_segments(segments: list, min_sentiment_score: float, min_duration: int = 60, max_duration: int = 90) -> list:
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

def generate_short_id():
    """Gera um ID curto baseado em um timestamp."""    
    return datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Retorna os primeiros 3 dígitos do milissegundos

def save_clips(video_path, selected_segments):
    """Salva os clipes selecionados em uma nova pasta com um ID curto."""    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    short_id = generate_short_id()  # Gera um ID curto
    clip_subfolder = CLIPS_DIR / f"{video_name}_{short_id}"  # Nova pasta para os clipes
    clip_subfolder.mkdir(parents=True, exist_ok=True)

    clips_saved = []

    for i, segment in enumerate(selected_segments):
        start_time = segment['start']
        end_time = segment['end']
        clip_filename = f"{video_name}_clip_{i + 1}.mp4"  # Nome do clipe
        clip_path = clip_subfolder / clip_filename

        try:
            video = mp.VideoFileClip(str(video_path))
            clip = video.subclip(start_time, end_time)
            clip.write_videofile(str(clip_path), codec="libx264")
            clips_saved.append(clip_path)
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

def process_video(video_path):
    """Processa o vídeo completo, extraindo o áudio, transcrevendo, selecionando e salvando clipes."""
    audio_output_path = AUDIO_DIR / f"{Path(video_path).stem}.mp3"
    try:
        extract_audio(video_path, audio_output_path)

        # Carregar o modelo Whisper do config.json
        whisper_model = whisper.load_model(config['whisper_model'])
        segments = transcribe_audio(audio_output_path, whisper_model)

        selected_segments = select_best_segments(
            segments, 
            config['video_processing']['min_sentiment_score'], 
        )

        if selected_segments:
            subtitle_path = save_subtitles(selected_segments, video_path, SUBTITLE_DIR)
            clips_saved = save_clips(video_path, selected_segments)

            # Log resumido e final
            logging.info(f"Processamento concluído: {len(selected_segments)} segmentos escolhidos, {len(clips_saved)} clipes salvos.")
    
    except Exception as e:
        logging.error(f"Erro no processamento do vídeo: {e}")
    finally:
        # Limpar os arquivos de áudio mesmo em caso de erro
        clean_up_audio_files()

# Chamando a função process_video com o caminho do vídeo
if __name__ == "__main__":
    video_file_path = sys.argv[1]
    process_video(video_file_path)
