#!/bin/bash

VIDEO_PATH="/mnt/c/Users/Kaio/workspace/jKpCutPro/videos/teste1.mp4"
SUBTITLE_OUTPUT_DIR="/mnt/c/Users/Kaio/workspace/jKpCutPro/subtitles"
MIN_SENTIMENT_SCORE="0.8"  # Adicionando o valor mínimo para o sentimento

# Passando todos os parâmetros necessários
python3 main.py "$VIDEO_PATH" "$SUBTITLE_OUTPUT_DIR" "$MIN_SENTIMENT_SCORE"
