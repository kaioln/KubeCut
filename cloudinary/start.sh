#!/bin/bash

# Caminho para o arquivo de vídeo
VIDEO_PATH="/mnt/c/Users/TI/Project/cloudinary/videos/teste1.mp4"

# Verifica se o arquivo de vídeo existe
if [ ! -f "$VIDEO_PATH" ]; then
  echo "O arquivo de vídeo não foi encontrado: $VIDEO_PATH"
  exit 1
fi

echo "Verificando o caminho do vídeo..."
echo "Executando o script de corte de vídeo..."

# Executa o script Python
python3 main.py "$VIDEO_PATH"
