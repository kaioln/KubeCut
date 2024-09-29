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

# Suprimir avisos da biblioteca transformers
hf_logging.set_verbosity_error()
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent
SUBTITLE_DIR = BASE_DIR / "subtitles"
CLIPS_DIR = BASE_DIR / "clips"
LOGS_DIR = BASE_DIR / "logs"
VIDEOS_DIR = BASE_DIR / "videos"

def load_config():
    """Carrega as configurações do arquivo JSON."""
    with open('config.json', 'r') as f:
        return json.load(f)

# Carrega as configurações
config = load_config()

def ensure_directories_exist():
    """Garante que as pastas necessárias existam antes de configurar o logging."""
    directories = [SUBTITLE_DIR, CLIPS_DIR, LOGS_DIR, VIDEOS_DIR]
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
sentiment_analyzer = pipeline("sentiment-analysis", model=config['sentiment_model'])
emotion_analyzer = pipeline("text-classification", model=config['emotion_model'])

# Carrega o modelo de NER com ajuste para ignorar pesos não correspondentes
from transformers import BertForTokenClassification, BertTokenizer

ner_model = BertForTokenClassification.from_pretrained(
    config['ner_model'],
    ignore_mismatched_sizes=True
)

# Carrega o tokenizer correspondente ao modelo NER
ner_tokenizer = BertTokenizer.from_pretrained(config['ner_model'])

# Inicializa o pipeline de NER com o modelo e tokenizer especificados
ner_analyzer = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")

def clean_text(text):
    """Remove caracteres especiais e limpa o texto."""
    return re.sub(r'\s+', ' ', text).strip()

def extract_audio(video_path, audio_output_path):
    """Extrai o áudio de um vídeo e salva em um arquivo."""
    logging.info(f"Extraindo áudio do vídeo: {video_path}")
    try:
        video = mp.VideoFileClip(str(video_path))
        audio = video.audio
        audio.write_audiofile(str(audio_output_path))
        logging.info(f"Áudio extraído e salvo em: {audio_output_path}")
    except Exception as e:
        logging.error(f"Erro ao extrair áudio: {e}")
        raise

def transcribe_audio(audio_path):
    """Transcreve o áudio utilizando o modelo Whisper."""
    logging.info(f"Iniciando a transcrição do áudio: {audio_path}")
    try:
        model = whisper.load_model(config['whisper_model'])
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

def save_subtitles(segments, video_path, output_dir, unique_id):
    """Salva os segmentos transcritos como um arquivo SRT com ID único."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_filename = f"{video_name}_{unique_id}.srt"
    subtitle_path = output_dir / subtitle_filename

    logging.info(f"Salvando a transcrição como legenda em: {subtitle_path}")
    try:
        with open(subtitle_path, 'w') as f:
            for i, segment in enumerate(segments):
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                text = segment['text']

                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text.strip()}\n\n")

        logging.info(f"Legenda salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda: {e}")
        raise

def analyze_sentiment(text: str):
    """Analisa o sentimento de um texto e retorna o rótulo e o score."""
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

def extract_topics(segments, num_topics=5, num_keywords=10):
    text_data = [segment['text'] for segment in segments if segment['text'].strip()]
    num_documents = len(text_data)

    if num_documents < 2:
        raise ValueError("O número de segmentos é muito pequeno para extrair tópicos.")

    # Ajuste dinâmico de min_df e max_df
    min_df = max(1, num_documents // 10)  # Ajusta min_df baseado em uma fração dos documentos
    max_df = min(0.95, num_documents - 1)  # Ajusta max_df para evitar conflitos

    try:
        vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, stop_words='english')
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

def select_best_segments(segments: list, min_sentiment_score: float, max_segments: int = 5, min_duration: int = 60, max_duration: int = 90) -> list:
    """Seleciona os melhores segmentos com base na análise de sentimentos e duração, garantindo cortes fluidos."""
    selected_segments = []

    # Extrair tópicos para todos os segmentos
    topics = extract_topics(segments)

    for segment in segments:
        text = clean_text(segment['text'])
        label, score = analyze_sentiment(text)
        duration = segment['end'] - segment['start']

        if score >= min_sentiment_score:
            segment['sentiment'] = label
            segment['sentiment_score'] = score
            segment['topics'] = topics
            selected_segments.append(segment)

    return combine_segments(selected_segments, min_duration, max_duration, max_segments)

def combine_segments(selected_segments, min_duration, max_duration, max_segments):
    """Combina segmentos adjacentes em cortes válidos."""
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
            current_segment = [segment]
            current_duration = segment_duration
            current_start_time = segment['start']

    if current_duration >= min_duration:
        combined_segments.append(create_combined_segment(current_segment, current_start_time))

    ranked_segments = sorted(combined_segments, key=lambda seg: seg['sentiment_score'], reverse=True)
    final_segments = ranked_segments[:max_segments]

    logging.info(f"Selecionados {len(final_segments)} cortes com duração entre {min_duration/60:.2f} e {max_duration/60:.2f} minutos.")
    return final_segments

def create_combined_segment(current_segment, start_time):
    """Cria um segmento combinado a partir de segmentos atuais."""
    return {
        'start': start_time,
        'end': current_segment[-1]['end'],
        'text': ' '.join(seg['text'].strip() for seg in current_segment),
        'sentiment_score': sum(seg['sentiment_score'] for seg in current_segment),
        'total_duration': sum(seg['end'] - seg['start'] for seg in current_segment)
    }

def save_cuts(segments, video_path, output_dir, unique_id):
    """Salva os grupos de segmentos como um arquivo SRT editado."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    clip_subdir = output_dir / f"{unique_id}"  # Nome da subpasta com base no unique_id
    clip_subdir.mkdir(parents=True, exist_ok=True)  # Cria a subpasta se não existir

    for i, segment in enumerate(segments):
        cut_filename = f"{video_name}_cut_{unique_id}_{i+1}.mp4"
        cut_path = clip_subdir / cut_filename  # Usar a subpasta para salvar os clips

        start_time = segment['start']
        end_time = segment['end']
        logging.info(f"Cortando vídeo de {start_time} a {end_time}, salvando como: {cut_path}")

        try:
            video = mp.VideoFileClip(str(video_path)).subclip(start_time, end_time)
            video.write_videofile(str(cut_path), codec='libx264', audio_codec='aac', remove_temp=True)
            logging.info(f"Corte salvo com sucesso em: {cut_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar o corte: {e}")
            raise

def main(video_path):
    """Função principal que orquestra a extração, transcrição, análise e corte de vídeo."""
    logging.info(f"Iniciando o processamento do vídeo: {video_path}")

    unique_id = generate_unique_id()
    audio_output_path = SUBTITLE_DIR / f"audio_{unique_id}.mp3"

    # Ler configurações antes de usar
    min_sentiment_score = config['video_processing']['min_sentiment_score']
    max_segments = config['video_processing']['max_segments']

    # Processar o vídeo
    extract_audio(video_path, audio_output_path)
    segments = transcribe_audio(audio_output_path)

    # Selecionar os melhores segmentos antes de salvar as legendas
    best_segments = select_best_segments(segments, min_sentiment_score, max_segments=max_segments)

    # Salvar legendas com base nos melhores segmentos
    subtitle_path = save_subtitles(best_segments, video_path, SUBTITLE_DIR, unique_id)

    # Salvar os cortes
    save_cuts(best_segments, video_path, CLIPS_DIR, unique_id)

    # Limpeza final
    os.remove(audio_output_path)
    logging.info(f"Áudio temporário removido: {audio_output_path}")
    logging.info("Processo concluído com sucesso.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python process_video.py <caminho_do_video>")
        sys.exit(1)

    video_file_path = Path(sys.argv[1])
    if not video_file_path.is_file():
        print(f"O arquivo especificado não existe: {video_file_path}")
        sys.exit(1)

    main(video_file_path)
