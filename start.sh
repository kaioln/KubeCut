#!/bin/bash

VIDEO_PATH="/mnt/c/Users/TI/Project/videos/teste1.mp4"
SUBTITLE_OUTPUT_DIR="/mnt/c/Users/TI/Project/subtitles"
MIN_SENTIMENT_SCORE="0.8"

python3 main.py "$VIDEO_PATH" "$SUBTITLE_OUTPUT_DIR" "$MIN_SENTIMENT_SCORE"
