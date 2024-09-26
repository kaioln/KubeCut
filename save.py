import sys
import moviepy.editor as mp
import whisper
import os
import logging
from datetime import datetime
from transformers import pipeline

# Configuração do logging
log_filename = "/mnt/c/Users/TI/Project/logs/process.log"
logging.basicConfig(filename=log_filename, level=logging.INFO,  # Alterado para INFO
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_audio(video_path, audio_output_path):
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
    try:
        logging.info(f"Iniciando a transcrição do áudio: {audio_path}")
        model = whisper.load_model("small")  # Carregando o modelo base do Whisper
        result = model.transcribe(audio_path, verbose=True)
        logging.info("Transcrição concluída com sucesso")
        return result["segments"]
    except Exception as e:
        logging.error(f"Erro ao transcrever o áudio: {e}")
        raise

def format_time(seconds):
    """Formata o tempo em horas:minutos:segundos,milissegundos para o formato SRT"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def get_next_subtitle_number(output_dir, base_name):
    """Obtém o próximo número sequencial com dois dígitos para os arquivos de legendas"""
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
    try:
        # Extrai o nome do arquivo sem extensão
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
                f.write(f"{text}\n\n")
        
        logging.info(f"Legenda salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda: {e}")
        raise

def analyze_sentiment(text: str):
    """Analisa o sentimento de um texto usando um modelo específico da Hugging Face."""
    model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
    sentiment_analyzer = pipeline('sentiment-analysis', model=model_name)
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

def select_best_segments(segments: list, min_sentiment_score: float) -> list:
    """Seleciona os melhores segmentos com base na pontuação de sentimento."""
    selected_segments = []
    for segment in segments:
        text = segment['text']
        label, score = analyze_sentiment(text)
        if score >= min_sentiment_score:
            segment['sentiment'] = label
            segment['sentiment_score'] = score
            selected_segments.append(segment)
    return selected_segments

def group_segments(segments, max_duration=60):
    """Agrupa os segmentos em blocos lógicos com duração máxima."""
    grouped_segments = []
    current_group = []
    current_duration = 0
    
    for segment in segments:
        segment_duration = segment['end'] - segment['start']
        if current_duration + segment_duration > max_duration:
            if current_group:
                grouped_segments.append(current_group)
            current_group = [segment]
            current_duration = segment_duration
        else:
            current_group.append(segment)
            current_duration += segment_duration
    
    if current_group:
        grouped_segments.append(current_group)
    
    return grouped_segments

def save_cuts(groups, video_path, output_dir, suffix):
    try:
        # Extrai o nome do arquivo sem extensão
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        subtitle_number = get_next_subtitle_number(output_dir, video_name)
        subtitle_filename = f"{video_name}_{subtitle_number}{suffix}.srt"
        subtitle_path = os.path.join(output_dir, subtitle_filename)
        
        logging.info(f"Salvando a legenda editada como: {subtitle_path}")
        with open(subtitle_path, 'w') as f:
            for group in groups:
                start_time = format_time(group[0]['start'])
                end_time = format_time(group[-1]['end'])
                
                f.write(f"{group[0]['id']}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(" ".join([segment['text'] for segment in group]) + "\n\n")
        
        logging.info(f"Legenda editada salva com sucesso em: {subtitle_path}")
        return subtitle_path
    except Exception as e:
        logging.error(f"Erro ao salvar a legenda editada: {e}")
        raise

def transcribe_video(video_path, subtitle_output_dir, min_sentiment_score):
    try:
        audio_output_path = "temp_audio.wav"
        
        # Extraindo o áudio do vídeo
        extract_audio(video_path, audio_output_path)
        
        # Transcrevendo o áudio
        segments = transcribe_audio(audio_output_path)
        
        # Selecionando os melhores segmentos
        best_segments = select_best_segments(segments, min_sentiment_score)
        
        # Agrupando os segmentos
        grouped_segments = group_segments(best_segments)
        
        # Salvando a legenda editada
        cut_subtitle_path = save_cuts(grouped_segments, video_path, subtitle_output_dir, "Corte")
        
        # Limpando o arquivo de áudio temporário
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
