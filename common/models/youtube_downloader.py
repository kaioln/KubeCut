import os
import re
from yt_dlp import YoutubeDL
from common.models.configs import VIDEOS_DIR
from common.models.logginlog import log_message

def sanitize_filename(filename):
    """Remove caracteres inválidos do título do vídeo e substitui espaços por underscores."""
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized

def download_video_from_url(video_url):
    """Baixa o vídeo de um link específico do YouTube e retorna o caminho do arquivo."""
    try:
        log_message(f"Iniciando download do vídeo: {video_url}")

        # Configuração para obter o título do vídeo
        with YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'video_desconhecido')

        # Sanitizar título e caminho do arquivo
        sanitized_title = sanitize_filename(video_title)
        video_path = os.path.join(VIDEOS_DIR, f"{sanitized_title}.mp4")
        
        if os.path.exists(video_path):
            log_message(f"Vídeo já foi baixado anteriormente: {video_path}", level="WARNING")
            return video_path

        # Opções para o yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': video_path,
            'noplaylist': True,
        }

        # Faz o download
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        log_message(f"Vídeo baixado com sucesso em: {video_path}")
        return video_path

    except Exception as e:
        log_message(f"Erro ao baixar o vídeo: {e}", level="ERROR")
        return None
