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

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBTITLE_DIR = os.path.join(BASE_DIR, "subtitles")
CLIPS_DIR = os.path.join(BASE_DIR, "clips")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

def ensure_directories_exist():
    """Garante que as pastas necessárias existam antes de configurar o logging."""
    directories = [SUBTITLE_DIR, CLIPS_DIR, LOGS_DIR, VIDEOS_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

ensure_directories_exist()

# Configuração do logging
log_filename = os.path.join(LOGS_DIR, "process.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializa os pipelines
os.environ["TOKENIZERS_PARALLELISM"] = "false"
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
ner_analyzer = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def clean_text(text):
    """Remove caracteres especiais e limpa o texto."""
    return re.sub(r'\s+', ' ', text).strip()

def extract_audio(video_path, audio_output_path):
    """Extrai o áudio de um vídeo e salva em um arquivo."""
    logging.info(f"Extraindo áudio do vídeo: {video_path}")
    try:
        video = mp.VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_output_path)
        logging.info(f"Áudio extraído e salvo em: {audio_output_path}")
    except Exception as e:
        logging.error(f"Erro ao extrair áudio: {e}")
        raise

def transcribe_audio(audio_path):
    """Transcreve o áudio utilizando o modelo Whisper."""
    logging.info(f"Iniciando a transcrição do áudio: {audio_path}")
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, verbose=True)
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
    subtitle_path = os.path.join(output_dir, subtitle_filename)

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
    min_df = 2
    max_df = 0.95

    if num_documents < min_df:
        min_df = 1  # Se houver poucos documentos, o min_df é ajustado para 1
    if min_df >= num_documents:
        min_df = num_documents - 1 if num_documents > 1 else 1  # Evitar conflito com max_df

    # Verificar se max_df é viável para o número de documentos
    if num_documents < 5:
        max_df = 0.85  # Diminuir max_df se houver poucos documentos

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
        print(f"Erro ao ajustar o vectorizer: {str(e)}")
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
    subtitle_filename = f"{video_name}_{unique_id}.srt"
    subtitle_path = os.path.join(output_dir, subtitle_filename)

    logging.info(f"Salvando a legenda editada como: {subtitle_path}")
    try:
        with open(subtitle_path, 'w') as f:
            for i, segment in enumerate(segments):
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                cut_duration = segment['end'] - segment['start']
                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time} (Duração total: {format_time(cut_duration)})\n")
                f.write(segment['text'].strip() + "\n\n")

        logging.info(f"Legenda editada salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda editada: {e}")
        raise

def cut_video(video_path, segments, clips_output_base_dir, unique_id, margin=0.5):
    """Corta o vídeo de acordo com os segmentos especificados e salva na subpasta com o ID único."""
    
    # Criar uma subpasta com o ID único na pasta "clips"
    output_dir = os.path.join(clips_output_base_dir, unique_id)
    os.makedirs(output_dir, exist_ok=True)

    logging.info(f"Cortando vídeo: {video_path}")
    video = mp.VideoFileClip(video_path)

    for i, segment in enumerate(segments):
        start_time = max(0, segment['start'] - margin)  # Garantir que não seja negativo
        end_time = segment['end'] + margin
        output_filename = os.path.join(output_dir, f"{unique_id}_clip_{i + 1}.mp4")

        logging.info(f"Cortando segmento: {start_time:.2f} - {end_time:.2f} e salvando como {output_filename}")
        video.subclip(start_time, end_time).write_videofile(output_filename, codec="libx264", audio_codec="aac")

    video.close()
    logging.info(f"Cortes de vídeo salvos em: {output_dir}")

def delete_audio_file(audio_path):
    """Remove o arquivo de áudio após o término do processo."""
    if os.path.exists(audio_path):
        try:
            os.remove(audio_path)
            logging.info(f"Arquivo de áudio {audio_path} removido com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao tentar remover o arquivo de áudio {audio_path}: {e}")

def main(video_path, min_sentiment_score=0.5, max_segments=5, min_duration=60, max_duration=90):
    """Função principal para processar o vídeo e gerar legendas e cortes."""
    unique_id = generate_unique_id()
    audio_path = os.path.join(VIDEOS_DIR, f"{unique_id}.mp3")

    # Extraindo áudio
    extract_audio(video_path, audio_path)

    # Transcrevendo áudio
    segments = transcribe_audio(audio_path)

    # Selecionando os melhores segmentos
    best_segments = select_best_segments(segments, min_sentiment_score, max_segments, min_duration, max_duration)

    # Salvando os cortes (legendas das melhores falas)
    save_cuts(best_segments, video_path, SUBTITLE_DIR, unique_id)

    # Cortando vídeo com as melhores falas
    cut_video(video_path, best_segments, CLIPS_DIR, unique_id)

    # Deletando o arquivo de áudio após o término do processo
    delete_audio_file(audio_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Caminho do vídeo não fornecido.")
        sys.exit(1)

    video_path = sys.argv[1]
    main(video_path)