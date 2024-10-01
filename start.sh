#!/bin/bash

# Caminho base do projeto
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Carrega o arquivo de configuração config.json
CONFIG_FILE="$BASE_DIR/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Arquivo de configuração config.json não encontrado."
    exit 1
fi

# Diretórios definidos no config.json
VIDEOS_DIR=$(jq -r '.directories.videos' "$CONFIG_FILE")
VIDEOS_DIR="$BASE_DIR/$VIDEOS_DIR"

# Verifica se o diretório de vídeos existe
if [ ! -d "$VIDEOS_DIR" ]; then
    echo "O diretório de vídeos não existe: $VIDEOS_DIR"
    exit 1
fi

# Loop para processar todos os arquivos de vídeo no diretório
for VIDEO_PATH in "$VIDEOS_DIR"/*; do
    # Verifica se o arquivo é um arquivo regular e se é um vídeo
    if [ -f "$VIDEO_PATH" ] && [[ "$VIDEO_PATH" == *.mp4 || "$VIDEO_PATH" == *.mov ]]; then
        echo "Processando vídeo: $VIDEO_PATH"
        # Chama o script Python com o caminho do vídeo
        python "$BASE_DIR/main.py" "$VIDEO_PATH"
    fi
done

echo "Processamento concluído para todos os vídeos."
