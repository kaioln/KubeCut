import os
import moviepy.editor as mp
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
from common.models.client_api import client
from common.models.configs import AUDIO_DIR
from common.models.logginlog import log_message

def transcrible_audio(video_path):
    """Extrai o áudio do vídeo e faz a transcrição completa."""
    log_message("Dividindo áudio em partes menores...")
    
    audio_name = 'audio_temp.mp3'

    audio_output_path = os.path.join(AUDIO_DIR, audio_name)

    extract_audio(video_path, audio_output_path)

    audio_partes = dividir_audio(audio_output_path)
    os.remove(audio_output_path)  # Remove o áudio completo para economizar espaço

    log_message("Iniciando transcrição...")
    transcricao, segmentos = transcrever_audio_partes(audio_partes)
    return transcricao, segmentos

def extract_audio(video_path, audio_output_path):
    log_message(f"Extraindo áudio do vídeo: {video_path}")
    try:
        video = mp.VideoFileClip(str(video_path))
        audio = video.audio
        
        # Especificar o caminho de saída para o arquivo de áudio
        audio.write_audiofile(audio_output_path, codec="mp3", bitrate="192k", ffmpeg_params=["-ar", "44100"])
        log_message(f"Áudio extraído e salvo em: {audio_output_path}")
    except Exception as e:
        log_message(f"Erro ao extrair áudio: {e}", level="ERROR")
        raise

def dividir_audio(audio_path, intervalo=10 * 60):
    """Divide o áudio em partes menores de 'intervalo' segundos."""
    audio = AudioSegment.from_file(audio_path)
    duracao = len(audio) // 1000  # duração em segundos
    partes = []

    for i in range(0, duracao, intervalo):
        inicio = i * 1000
        fim = min((i + intervalo) * 1000, len(audio))
        parte = audio[inicio:fim]
        parte_path = os.path.join(AUDIO_DIR, f"audio_parte_{i // intervalo}.mp3")
        parte.export(parte_path, format="mp3")
        partes.append(parte_path)

    return partes

def transcrever_audio_partes(audio_partes):
    """Transcreve cada parte do áudio e retorna texto e segmentos."""
    transcricao_completa = ""
    todos_segmentos = []

    def transcrever(parte):
        with open(parte, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
            )
            return response.text, response.segments

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(transcrever, audio_partes)

    for transcricao_parcial, segmentos_parciais in results:
        transcricao_completa += transcricao_parcial + "\n"
        todos_segmentos.extend(segmentos_parciais)

    # Removendo os arquivos temporários de áudio após a transcrição
    for parte in audio_partes:
        if os.path.exists(parte):
            os.remove(parte)

    return transcricao_completa, todos_segmentos