import os
import logging
import re
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL
from pathlib import Path

# Configuração do logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('process.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Chave da API do YouTube
YOUTUBE_API_KEY = 'AIzaSyAcYrb9k3rHmYdvQcR1EO8MpBYPmHAYt7M'  # Substitua pela sua nova chave de API

def sanitize_filename(filename):
    """Remove caracteres inválidos do título do vídeo para salvar corretamente no sistema de arquivos."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_latest_video_from_channel(channel_id):
    """Retorna o último vídeo de um canal usando a API do YouTube, ignorando lives ao vivo."""
    try:
        logging.info("Inicializando a API do YouTube.")
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        # Pega os vídeos do canal
        logging.info(f"Buscando vídeos do canal ID: {channel_id}")
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            order='date',
            maxResults=5  # Buscar mais vídeos para evitar lives
        )
        response = request.execute()

        if response['items']:
            logging.info(f"Número de vídeos encontrados: {len(response['items'])}")
            for video in response['items']:
                live_content = video['snippet'].get('liveBroadcastContent')
                logging.info(f"Verificando se o vídeo é uma live: {video['snippet']['title']} ({live_content})")
                if live_content == 'live':
                    logging.info(f"Ignorando live ao vivo: {video['snippet']['title']}")
                    continue

                video_id = video['id'].get('videoId')
                if not video_id:
                    logging.warning(f"Vídeo sem ID válido encontrado: {video['snippet']['title']}")
                    continue

                video_title = video['snippet']['title']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                logging.info(f"Último vídeo válido encontrado: {video_title} ({video_url})")
                return video_url, video_title

            logging.error("Nenhum vídeo válido encontrado (somente lives ou vídeos sem ID).")
            return None, None
        else:
            logging.error("Nenhum vídeo encontrado no canal.")
            return None, None

    except Exception as e:
        logging.error(f"Erro ao acessar a API do YouTube: {str(e)}", exc_info=True)
        return None, None

def download_video(video_url, video_title):
    """Faz o download de um vídeo do YouTube usando yt-dlp e salva no diretório especificado."""
    try:
        logging.info(f"Iniciando download do vídeo: {video_title}")

        # Diretório onde o vídeo será salvo
        video_dir = Path('/mnt/c/Users/TI/Project/videos')
        video_dir.mkdir(parents=True, exist_ok=True)

        # Sanitizar o título do vídeo para criar um nome de arquivo válido
        sanitized_title = sanitize_filename(video_title)
        video_path = video_dir / f"{sanitized_title}.mp4"

        # Verifica se o vídeo já foi baixado
        if video_path.exists():
            logging.info(f"Vídeo já foi baixado anteriormente: {video_path}")
            return video_path

        # Opções para o yt-dlp
        ydl_opts = {
            'format': 'best',  # Baixar na melhor qualidade disponível
            'outtmpl': str(video_path),  # Define o caminho e o nome do arquivo
            'noplaylist': True,  # Não baixar playlists
        }

        # Faz o download do vídeo usando yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        logging.info(f"Vídeo baixado com sucesso em: {video_path}")
        return video_path

    except Exception as e:
        logging.error(f"Erro ao baixar o vídeo: {str(e)}", exc_info=True)
        return None

def process_latest_video():
    youtube_channel_id = "UC69JW8XvnPjXZfysWQqOk4Q"  # ID do canal desejado
    logging.info("Iniciando o processamento do último vídeo.")
    latest_video_url, latest_video_title = get_latest_video_from_channel(youtube_channel_id)

    if latest_video_url and latest_video_title:
        logging.info(f"Preparando para baixar o vídeo: {latest_video_title}")
        video_path = download_video(latest_video_url, latest_video_title)
        if video_path and os.path.exists(video_path):
            logging.info(f"Vídeo baixado com sucesso em: {video_path}")
            print(f"Vídeo baixado com sucesso em: {video_path}")
        else:
            logging.error("Falha no download do vídeo.")
            print("Falha no download do vídeo. Verifique os logs para mais detalhes.")
    else:
        logging.error("Nenhum vídeo foi encontrado para download.")
        print("Falha ao encontrar ou baixar o vídeo. Verifique os logs para mais detalhes.")

if __name__ == "__main__":
    process_latest_video()
