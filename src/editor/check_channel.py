import os
from googleapiclient.discovery import build
from common.models.client_api import yt_key
from common.models.logginlog import log_message
from common.models.youtube_downloader import download_video_from_url

log_message("----  INICIANDO LOGICA DE DOWNLOAD DO YOUTUBE ----")

def get_latest_video_from_channel(channel_id):
    """Retorna o último vídeo de um canal usando a API do YouTube, ignorando lives ao vivo."""
    try:
        log_message("Inicializando a API do YouTube.")
        youtube = build('youtube', 'v3', developerKey=yt_key)

        # Pega os vídeos do canal
        log_message(f"Buscando vídeos do canal ID: {channel_id}")
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            order='date',
            maxResults=5
        )
        response = request.execute()

        if response['items']:
            for video in response['items']:
                if video['snippet'].get('liveBroadcastContent') == 'live':
                    log_message(f"Ignorando live ao vivo: {video['snippet']['title']}")
                    continue

                video_id = video['id'].get('videoId')
                if video_id:
                    video_title = video['snippet']['title']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    log_message(f"Último vídeo válido encontrado: {video_title} ({video_url})")
                    return video_url

            log_message("Nenhum vídeo válido encontrado.", level="ERROR")
            return None
        else:
            log_message("Nenhum vídeo encontrado no canal.", level="ERROR")
            return None

    except Exception as e:
        log_message(f"Erro ao acessar a API do YouTube: {e}", level="ERROR")
        return None

def process_latest_video():
    youtube_channel_id = "UCs9Yzaw0aeNygsw42kjeP7g"  # ID do canal desejado
    log_message("Iniciando o processamento do último vídeo.")
    latest_video_url = get_latest_video_from_channel(youtube_channel_id)

    if latest_video_url:
        video_path = download_video_from_url(latest_video_url)
        if video_path and os.path.exists(video_path):
            log_message(f"Vídeo baixado com sucesso em: {video_path}")
            log_message("----  FINALIZANDO LOGICA DE DOWNLOAD DO YOUTUBE ----")
        else:
            log_message("Falha no download do vídeo.", level="ERROR")
    else:
        log_message("Nenhum vídeo foi encontrado para download.", level="ERROR")

if __name__ == "__main__":
    process_latest_video()
