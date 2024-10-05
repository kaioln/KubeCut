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

# Verifica se o comando 'jq' retornou um valor válido, caso contrário usa a segunda opção com 'python'
if [ -z "$VIDEOS_DIR" ] || [ "$VIDEOS_DIR" == "null" ]; then
    echo "Falha ao obter diretório de vídeos usando 'jq', tentando com 'python'..."
    CONFIG_FILE_WIN=$(echo "$CONFIG_FILE" | sed 's|/c/|C:/|g')
    VIDEOS_DIR=$(python -c "import json; f=open('$CONFIG_FILE_WIN'); config=json.load(f); print(config['directories']['videos'])")
    echo "Pasta detectada, iniciando ..."

    if [ -z "$VIDEOS_DIR" ]; then
        echo "Falha ao obter diretório de vídeos usando 'python'."
        exit 1
    fi
fi
VIDEOS_DIR="$BASE_DIR/$VIDEOS_DIR"

# Verifica se o diretório de vídeos existe
if [ ! -d "$VIDEOS_DIR" ]; then
    echo "O diretório de vídeos não existe. Criando diretório: $VIDEOS_DIR"
    mkdir -p "$VIDEOS_DIR"
    if [ $? -eq 0 ]; then
        echo "Diretório criado com sucesso. Coloque os vídeos em: $VIDEOS_DIR"
        echo "Reinicie o processo quando os vídeos estiverem no local informado."
        exit 1
    else
        echo "Erro ao criar o diretório: $VIDEOS_DIR"
        exit 1
    fi
fi

# Verifica se existe arquivo de vídeo na pasta
shopt -s nullglob
VIDEOS=("$VIDEOS_DIR"/*.mp4 "$VIDEOS_DIR"/*.mov)

if [ ${#VIDEOS[@]} -eq 0 ]; then
    echo "Nenhum vídeo encontrado no diretório: $VIDEOS_DIR"
    exit 1
fi

# Loop para processar todos os arquivos de vídeo no diretório
for VIDEO_PATH in "${VIDEOS[@]}"; do
    # Verifica se o arquivo é um arquivo regular e se é um vídeo
    if [ -f "$VIDEO_PATH" ]; then
        echo "Processando vídeo: $VIDEO_PATH"
        
        # Chama o script Python com o caminho do vídeo
        python "$BASE_DIR/main.py" "$VIDEO_PATH"
        
        echo "Processamento concluído para o vídeo: $VIDEO_PATH"
    fi
done