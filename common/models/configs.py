import json
import os

# Voltar duas pastas
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)), 
            os.pardir, 
            os.pardir)
)

def load_config():
    config_path = os.path.join(BASE_DIR, 'config', 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

config = load_config()

# Diretórios baseados no arquivo config.json
TEMP_DIR = os.path.join(BASE_DIR, 'data\\temp')
SUBTITLE_DIR = os.path.join(TEMP_DIR, config['directories']['subtitles'])
CLIPS_DIR = os.path.join(BASE_DIR, 'data\\output', config['directories']['clips'])
FINAL_DIR = os.path.join(BASE_DIR, 'data\\input', config['directories']['processed'])
LOGS_DIR = os.path.join(BASE_DIR, config['directories']['logs']['dir'])
VIDEOS_DIR = os.path.join(BASE_DIR, 'data\\input', config['directories']['videos'])
AUDIO_DIR = os.path.join(TEMP_DIR, config['directories']['audio'])
WORDS_DIR = os.path.join(BASE_DIR, 'common', config['directories']['prohibited_words']['dir'])

# Lista de diretórios a verificar/criar
directories = [TEMP_DIR, SUBTITLE_DIR, CLIPS_DIR, FINAL_DIR, LOGS_DIR, VIDEOS_DIR, AUDIO_DIR, WORDS_DIR]

# Função para verificar se os diretórios existem, e criá-los se não existirem
def ensure_directories_exist(dirs):
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Diretório criado: {directory}")

# Chamada da função para verificar/criar os diretórios
ensure_directories_exist(directories)
