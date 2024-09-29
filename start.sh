#!/bin/bash

# Caminho base do projeto
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Caminho do diretório de vídeos
VIDEOS_DIR="$BASE_DIR/videos"

# Verifica se o diretório de vídeos existe
if [ ! -d "$VIDEOS_DIR" ]; then
    echo "O diretório de vídeos não existe: $VIDEOS_DIR"
    exit 1
fi

# Loop para processar todos os arquivos de vídeo no diretório
for VIDEO_PATH in "$VIDEOS_DIR"/*; do
    # Verifica se o arquivo é um arquivo regular
    if [ -f "$VIDEO_PATH" ]; then
        echo "Processando vídeo: $VIDEO_PATH"
        # Chama o script Python com o caminho do vídeo como argumento
        python "$BASE_DIR/main.py" "$VIDEO_PATH"
    fi
done

echo "Processamento concluído para todos os vídeos."
