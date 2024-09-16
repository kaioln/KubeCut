#!/bin/bash

# Defina o diretório do projeto
PROJECT_DIR="/mnt/c/Users/TI/Project/video-editor-ai"

# Inicie o backend FastAPI na porta 8001
echo "Iniciando o backend FastAPI na porta 8001..."
cd "$PROJECT_DIR/backend"
uvicorn app.main:app --host 0.0.0.0 --port 8001 &

# Aguarde alguns segundos para garantir que o backend esteja pronto
sleep 5

# Inicie o servidor PHP para o frontend na porta 8000
echo "Iniciando o servidor PHP para o frontend na porta 8000..."
cd "$PROJECT_DIR/frontend"
php -S localhost:8000 -t . &

# Espera para que o script continue em execução
wait
