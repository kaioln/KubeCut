import os
import datetime
import subprocess
import sys
from common.models.configs import BASE_DIR, VIDEOS_DIR, FINAL_DIR, TEMP_DIR
from common.models.logginlog import log_message
from common.utils.clear_temp import clean_temp_archives
from common.utils.database import save_log

# Caminho para o interpretador Python no ambiente virtual
python_interpreter = os.path.join(BASE_DIR, '.venv', 'Scripts', 'python.exe')
if not os.path.exists(python_interpreter):
    log_message("Ambiente virtual não encontrado.", level="INFO")
    sys.exit(1)

# Função para garantir que o diretório exista
def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        log_message(f"Diretório criado: {path}")

# Função para verificar a existência de arquivos de vídeo no diretório
def check_video_files(videos_dir):
    video_formats = ('.mp4', '.mov')
    return [file for file in os.listdir(videos_dir) if file.endswith(video_formats)]

# Função para baixar vídeo do YouTube
def download_video():
    log_message("Iniciando o download do último vídeo do YouTube...", level="INFO")
    subprocess.run([python_interpreter, '-m', 'src.youtube_download'], check=True)

# Função para processar o vídeo chamando o main.py
def process_video(video_path):
    log_message(f"Processando vídeo: {video_path}", level="INFO")
    subprocess.run([python_interpreter, '-m', 'src.main', video_path], check=True)
    
    clean_temp_archives(TEMP_DIR)

    log_message(f"Processamento concluído para o vídeo: {video_path}", level="INFO")

# Checa se há vídeo ou baixa um novo
videos = check_video_files(VIDEOS_DIR)
if not videos:
    download_video()
    videos = check_video_files(VIDEOS_DIR)

# Processa os vídeos
for video_file in videos:
    video_path = os.path.join(VIDEOS_DIR, video_file)
    process_video(video_path)

    # Renomeia e move o arquivo processado
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{os.path.splitext(video_file)[0]}_{timestamp}.mp4"
    destination_path = os.path.join(FINAL_DIR, new_filename)
    
    if os.path.exists(destination_path):
        log_message(f"O arquivo {new_filename} já existe no diretório {FINAL_DIR}.", level="INFO")
    else:
        os.rename(video_path, destination_path)  # Descomente para mover o vídeo
        log_message(f"Arquivo {video_file} movido para: {destination_path}", level="INFO")
