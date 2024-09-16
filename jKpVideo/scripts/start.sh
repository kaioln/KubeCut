#!/bin/bash

VIDEO_PATH="/mnt/c/Users/TI/Project/jKpVideo/videos/teste1.mp4"
SCENE_CHANGES_FILE="/mnt/c/Users/TI/Project/jKpVideo/videos/scene_changes.txt"
OUTPUT_FOLDER="/mnt/c/Users/TI/Project/jKpVideo/videos/clips"

echo "Detectando mudanças de cena..."
python3 /mnt/c/Users/TI/Project/jKpVideo/scripts/detect_scenes.py "$VIDEO_PATH" "$SCENE_CHANGES_FILE"

echo "Cortando e redimensionando clipes..."
python3 /mnt/c/Users/TI/Project/jKpVideo/scripts/process_video.py "$VIDEO_PATH" "$SCENE_CHANGES_FILE" "$OUTPUT_FOLDER"

echo "Processo concluído! Verifique os clipes na pasta '$OUTPUT_FOLDER'."
