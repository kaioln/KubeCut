import sys
import os
import logging
import re
from datetime import datetime
import moviepy.editor as mp
import whisper
from transformers import pipeline

# Caminho base do projeto
BASE_DIR = "/mnt/c/Users/Kaio/workspace/jKpCutPro"
SUBTITLE_DIR = os.path.join(BASE_DIR, "subtitles")
CLIPS_DIR = os.path.join(BASE_DIR, "clips")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

# Configuração do logging
log_filename = os.path.join(LOGS_DIR, "process.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ensure_directories_exist():
    """Garante que as pastas necessárias existam."""
    directories = [
        SUBTITLE_DIR,
        CLIPS_DIR,
        LOGS_DIR,
        VIDEOS_DIR
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Pasta verificada/criada: {directory}")

# Chamando a função para garantir que as pastas existem
ensure_directories_exist()

# Inicializa o pipeline de análise de sentimentos
os.environ["TOKENIZERS_PARALLELISM"] = "false"
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

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

def select_best_segments(segments: list, min_sentiment_score: float, max_segments: int = 5, min_duration: int = 60, max_duration: int = 90) -> list:
    """Seleciona os melhores segmentos com base na análise de sentimentos e duração, garantindo cortes fluidos."""
    selected_segments = []

    for segment in segments:
        text = clean_text(segment['text'])
        label, score = analyze_sentiment(text)
        duration = segment['end'] - segment['start']

        if score >= min_sentiment_score:
            segment['sentiment'] = label
            segment['sentiment_score'] = score
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

def save_cuts(segments, video_path, output_dir, suffix, unique_id):
    """Salva os grupos de segmentos como um arquivo SRT editado."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_filename = f"{video_name}_{unique_id}_{suffix}.srt"
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
    clips_output_dir = os.path.join(clips_output_base_dir, unique_id)
    os.makedirs(clips_output_dir, exist_ok=True)  # Cria a subpasta com o ID

    video = mp.VideoFileClip(video_path)
    
    for i, segment in enumerate(segments):
        start_time = segment['start']
        end_time = segment['end'] + margin  # Adiciona uma margem de tempo para evitar cortes abruptos
        cut_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_cut_{i + 1}.mp4"
        cut_path = os.path.join(clips_output_dir, cut_filename)

        logging.info(f"Cortando o vídeo de {format_time(start_time)} até {format_time(end_time)}.")
        try:
            video.subclip(start_time, end_time).write_videofile(cut_path, codec="libx264")
            logging.info(f"Corte salvo em: {cut_path}")
        except Exception as e:
            logging.error(f"Erro ao cortar o vídeo: {e}")

if __name__ == "__main__":
    # Uso do script
    video_path = sys.argv[1]
    
    # Criar arquivos necessários
    unique_id = generate_unique_id()
    audio_output_path = os.path.join(BASE_DIR, f"{unique_id}_audio.wav")
    
    try:
        extract_audio(video_path, audio_output_path)
        segments = transcribe_audio(audio_output_path)
        
        # Selecionar os melhores segmentos
        selected_segments = select_best_segments(segments, min_sentiment_score=0.5)

        # Salvar os cortes de vídeo com o único arquivo SRT
        save_cuts(selected_segments, video_path, SUBTITLE_DIR, "edited", unique_id)
        cut_video(video_path, selected_segments, CLIPS_DIR, unique_id)
    
    except Exception as e:
        logging.error(f"Ocorreu um erro no processamento do vídeo: {e}")

    finally:
        # Remover o arquivo de áudio temporário
        if os.path.exists(audio_output_path):
            os.remove(audio_output_path)
            logging.info(f"Arquivo de áudio temporário removido: {audio_output_path}")


