import sys
import moviepy.editor as mp
import whisper
import os
import logging
from datetime import datetime
from transformers import pipeline
import re

# Configuração do logging
log_filename = "/mnt/c/Users/TI/Project/logs/process.log"
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializa o pipeline de análise de sentimentos
sentiment_analyzer = pipeline("sentiment-analysis")

def clean_text(text):
    """Remove caracteres especiais e limpa o texto."""
    text = re.sub(r'\s+', ' ', text)  # Remove múltiplos espaços
    return text.strip()

def extract_audio(video_path, audio_output_path):
    """Extrai o áudio de um vídeo e salva em um arquivo."""
    try:
        logging.info(f"Extraindo áudio do vídeo: {video_path}")
        video = mp.VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_output_path)
        logging.info(f"Áudio extraído e salvo em: {audio_output_path}")
    except Exception as e:
        logging.error(f"Erro ao extrair áudio: {e}")
        raise

def transcribe_audio(audio_path):
    """Transcreve o áudio utilizando o modelo Whisper."""
    try:
        logging.info(f"Iniciando a transcrição do áudio: {audio_path}")
        model = whisper.load_model("medium")  # Usando o modelo 'medium' para melhor precisão
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

def get_next_subtitle_number(output_dir, base_name):
    """Obtém o próximo número de legenda disponível para salvar."""
    existing_files = [f for f in os.listdir(output_dir) if f.startswith(base_name) and f.endswith('.srt')]
    numbers = []
    for file in existing_files:
        try:
            number = int(file.split('_')[-1].split('.')[0])
            numbers.append(number)
        except ValueError:
            continue
    next_number = max(numbers, default=0) + 1
    return f"{next_number:02}"

def save_subtitles(segments, video_path, output_dir):
    """Salva os segmentos transcritos como um arquivo SRT."""
    try:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        subtitle_number = get_next_subtitle_number(output_dir, video_name)
        subtitle_filename = f"{video_name}_{subtitle_number}.srt"
        subtitle_path = os.path.join(output_dir, subtitle_filename)

        logging.info(f"Salvando a transcrição como legenda em: {subtitle_path}")
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

def select_best_segments(segments: list, min_sentiment_score: float, max_segments: int = 5, min_duration: int = 24, max_duration: int = 60) -> list:
    """Seleciona os melhores segmentos com base na análise de sentimentos e duração."""
    selected_segments = []

    for segment in segments:
        text = clean_text(segment['text'])
        label, score = analyze_sentiment(text)
        duration = segment['end'] - segment['start']
        
        if score >= min_sentiment_score and min_duration <= duration <= max_duration:
            segment['sentiment'] = label
            segment['sentiment_score'] = score
            selected_segments.append(segment)

    # Ordena os segmentos pelo score de sentimento, do maior para o menor
    selected_segments.sort(key=lambda x: x['sentiment_score'], reverse=True)

    # Se houver menos de 5 segmentos, completa com os segmentos restantes, independente do score
    if len(selected_segments) < max_segments:
        logging.warning(f"Menos de {max_segments} segmentos atendem aos critérios. Selecionando segmentos adicionais.")
        remaining_segments = [seg for seg in segments if seg not in selected_segments]
        selected_segments += remaining_segments[:max_segments - len(selected_segments)]

    # Seleciona até max_segments
    final_segments = selected_segments[:max_segments]

    logging.info(f"Selecionados {len(final_segments)} segmentos com duração entre {min_duration} e {max_duration} segundos.")
    return final_segments

def save_cuts(segments, video_path, output_dir, suffix):
    """Salva os grupos de segmentos como um arquivo SRT editado.""" 
    try:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        subtitle_number = get_next_subtitle_number(output_dir, video_name)
        subtitle_filename = f"{video_name}_{subtitle_number}_{suffix}.srt"
        subtitle_path = os.path.join(output_dir, subtitle_filename)

        logging.info(f"Salvando a legenda editada como: {subtitle_path}")
        with open(subtitle_path, 'w') as f:
            for i, segment in enumerate(segments):
                start_time = format_time(segment['start'])
                end_time = format_time(segment['end'])
                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(segment['text'].strip() + "\n\n")

        logging.info(f"Legenda editada salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda editada: {e}")
        raise

def transcribe_video(video_path, subtitle_output_dir, min_sentiment_score):
    """Transcreve o vídeo e salva as legendas editadas com os melhores segmentos."""
    try:
        audio_output_path = "temp_audio.wav"
        
        extract_audio(video_path, audio_output_path)
        segments = transcribe_audio(audio_output_path)
        best_segments = select_best_segments(segments, min_sentiment_score)
        
        if best_segments:
            cut_subtitle_path = save_cuts(best_segments, video_path, subtitle_output_dir, "Corte")
        else:
            logging.warning("Nenhum segmento foi selecionado com base nos critérios definidos.")
            return None
        
        if os.path.exists(audio_output_path):
            os.remove(audio_output_path)
        
        logging.info(f"Processo de transcrição concluído com sucesso. Legenda editada salva em: {cut_subtitle_path}")
        return cut_subtitle_path
    except Exception as e:
        logging.error(f"Erro durante o processo de transcrição: {e}")
        raise

if __name__ == "__main__":    
    if len(sys.argv) != 4:
        logging.error("Uso incorreto. Deve ser: python3 main.py <video_path> <subtitle_output_dir> <min_sentiment_score>")
        print("Uso: python3 main.py <video_path> <subtitle_output_dir> <min_sentiment_score>")
        sys.exit(1)

    video_path = sys.argv[1]
    subtitle_output_dir = sys.argv[2]
    min_sentiment_score = float(sys.argv[3])

    try:
        cut_subtitle_path = transcribe_video(video_path, subtitle_output_dir, min_sentiment_score)
        print("Legenda editada salva em:", cut_subtitle_path)
    except Exception as e:
        logging.error(f"Falha ao processar o vídeo: {e}")
        print("Ocorreu um erro. Verifique o arquivo de log para mais detalhes.")
