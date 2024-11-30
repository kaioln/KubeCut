import random
import os
from common.utils.extract_excerpt import extract_theme
from common.models.configs import SONGS_DIR

def select_background_music(text):

    theme = extract_theme(text)
    # Mapeamento de temas para trilhas sonoras
    music_library = {
        "CALMO": ["calmo.mp3", "calmo2.mp3"],
        "INSPIRACAO": ["inspiracao.mp3", "inspiracao2.mp3"],
        "MELANCOLICO": ["melancolico.mp3", "melancolico2.mp3"],
        "SUSPENSE": ["suspense.mp3", "suspense2.mp3"]
    }
    # Obtém a lista de músicas associadas ao tema
    music_files = music_library.get(theme.lower(), ["default_background.mp3"])

    # Concatena o diretório SONGS_DIR ao nome do arquivo de música
    music_path = os.path.join(SONGS_DIR, random.choice(music_files))

    print(music_path)
    print("music_files")
    # Retorna o caminho completo do arquivo de música
    return music_path
