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
FINAL_DIR=$(jq -r '.directories.processed' "$CONFIG_FILE")

# Verifica se o comando 'jq' retornou um valor válido
if [ -z "$VIDEOS_DIR" ] || [ "$VIDEOS_DIR" == "null" ] || [ -z "$FINAL_DIR" ] || [ "$FINAL_DIR" == "null" ]; then
    echo "Falha ao obter diretórios usando 'jq', tentando com 'python'..."
    CONFIG_FILE_WIN=$(echo "$CONFIG_FILE" | sed 's|/c/|C:/|g')
    VIDEOS_DIR=$(python -c "import json; f=open('$CONFIG_FILE_WIN'); config=json.load(f); print(config['directories']['videos'])")
    FINAL_DIR=$(python -c "import json; f=open('$CONFIG_FILE_WIN'); config=json.load(f); print(config['directories']['processed'])")
    echo "Iniciando processamento de videos"
    
    if [ -z "$VIDEOS_DIR" ]; then
        echo "Falha ao obter diretórios usando 'python'."
        exit 1
    fi
fi
VIDEOS_DIR="$BASE_DIR/$VIDEOS_DIR"

# Verifica se o diretório de vídeos existe, se não, cria
if [ ! -d "$VIDEOS_DIR" ]; then
    echo "O diretório de vídeos não existe. Criando diretório: $VIDEOS_DIR"
    mkdir -p "$VIDEOS_DIR"
    if [ $? -eq 0 ]; then
        echo "Diretório criado com sucesso. Coloque os vídeos em: $VIDEOS_DIR"
        echo "Reiniciando o processo..."
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
    echo "Iniciando o download do último vídeo do YouTube..."
    
    # Chama o script para baixar o vídeo do YouTube
    python "$BASE_DIR/youtube_download.py"  # Substitua pelo seu script de download

    # Recarrega a lista de vídeos após o download
    VIDEOS=("$VIDEOS_DIR"/*.mp4 "$VIDEOS_DIR"/*.mov)

    if [ ${#VIDEOS[@]} -eq 0 ]; then
        echo "Nenhum vídeo encontrado após o download."
        exit 1
    fi
fi

if [ ! -d "$VIDEOS_DIR/$FINAL_DIR" ]; then
    echo "O diretório final não existe. Criando diretório: $VIDEOS_DIR/$FINAL_DIR"
    mkdir -p "$VIDEOS_DIR/$FINAL_DIR"
    if [ $? -eq 0 ]; then
        echo "Diretório criado com sucesso. Os arquivos serão movidos para a pasta: $FINAL_DIR"
    else
        echo "Erro ao criar o diretório: $VIDEOS_DIR/$FINAL_DIR"
        exit 1
    fi
fi

# Loop para processar todos os arquivos de vídeo no diretório
for VIDEO_PATH in "${VIDEOS[@]}"; do
    if [ -f "$VIDEO_PATH" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - INFO - Processando vídeo: $VIDEO_PATH" >> "$BASE_DIR/logs/process.log"

        # Chama o script Python com o caminho do vídeo
        python "$BASE_DIR/main.py" "$VIDEO_PATH"

        FILENAME=$(basename "$VIDEO_PATH")
        EXTENSION="${FILENAME##*.}"
        NAME="${FILENAME%.*}"
        TIMESTAMP=$(date '+%Y%m%d%H%M%S')
        NEW_FILENAME="${NAME}_${TIMESTAMP}.${EXTENSION}"
        DESTINATION="$VIDEOS_DIR/$FINAL_DIR/$NEW_FILENAME"

        if [ -e "$DESTINATION" ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - WARNING - O arquivo $NEW_FILENAME já existe em $FINAL_DIR. O arquivo não foi movido." >> "$BASE_DIR/logs/process.log"
        else
            mv "$VIDEO_PATH" "$DESTINATION" # HABILITAR DEPOIS SO PRA N FICAR MEXENDO COM VIDEO
            if [ $? -eq 0 ]; then
                echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - INFO - O arquivo $VIDEO_PATH foi movido com sucesso para: $DESTINATION" >> "$BASE_DIR/logs/process.log"
            else
                echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - ERROR - Erro ao mover o arquivo $VIDEO_PATH para: $DESTINATION" >> "$BASE_DIR/logs/process.log"
            fi
        fi

        echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - INFO - Processamento concluído para o vídeo: $VIDEO_PATH" >> "$BASE_DIR/logs/process.log"
        echo "Processamento concluído para o vídeo: $VIDEO_PATH"
    fi
done