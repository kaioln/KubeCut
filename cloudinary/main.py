import os
import sys
import logging
import openai_whisper
from moviepy.editor import VideoFileClip
import json
import tempfile

# Setup logging
logging.basicConfig(filename="logs/process.log", level=logging.INFO, format="%(asctime)s %(message)s")

# Whisper Model Initialization
whisper_model = openai_whisper.load_model("base")

def transcribe_audio(video_path):
    """
    Transcribe audio from the video using OpenAI Whisper.
    """
    logging.info("Transcribing audio from video.")

    # Extract audio from video
    with VideoFileClip(video_path) as video:
        audio_path = f"{os.path.splitext(video_path)[0]}.wav"
        video.audio.write_audiofile(audio_path)
    
    # Transcribe audio file using Whisper
    try:
        result = whisper_model.transcribe(audio_path)
        transcription = result['text']
        logging.info("Transcription completed successfully.")
        return transcription
    except Exception as e:
        logging.error(f"Failed to transcribe audio {audio_path}: {e}")
        return ""

def analyze_transcription(transcription):
    """
    Analyze the transcription to identify important segments.
    """
    logging.info("Analyzing transcription to extract important moments.")
    
    # Placeholder for analysis (e.g., sentiment analysis or keyword extraction)
    # Dummy implementation: use entire video
    segments = [(0, 30)]  # Example: return fixed segments
    return segments

def generate_cuts(video_path, duration_min=21, duration_max=34):
    logging.info("Generating video cuts from the original video.")
    clips_generated = []

    try:
        video = VideoFileClip(video_path)
        video_duration = int(video.duration)
    except Exception as e:
        logging.error(f"Failed to load video {video_path}: {e}")
        return clips_generated

    transcription = transcribe_audio(video_path)
    important_segments = analyze_transcription(transcription)

    for start_time, end_time in important_segments:
        if end_time - start_time < duration_min:
            continue
        
        clip_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_clip_{start_time}.mp4"
        clip_path = os.path.join("clips", clip_filename)
        try:
            video.subclip(start_time, end_time).write_videofile(clip_path, codec="libx264")
            logging.info(f"Generated clip: {clip_path}")
            clips_generated.append(clip_path)
        except Exception as e:
            logging.error(f"Failed to generate clip {clip_path}: {e}")

    logging.info(f"Generated {len(clips_generated)} clips.")
    return clips_generated

def process_clips(clips):
    logging.info(f"Processing {len(clips)} clips for optimization.")
    
    for clip in clips:
        clip_path_resized = f"clips/resized_{os.path.basename(clip)}"
        with VideoFileClip(clip) as video:
            video_resized = video.resize(height=1080)  # Adjust height for vertical format
            video_resized.write_videofile(clip_path_resized, codec="libx264")
        
        video_url = upload_video_to_cloudinary(clip_path_resized)
        if video_url:
            optimized_url, _ = cloudinary_url(os.path.basename(clip_path_resized), fetch_format="auto", quality="auto")
            logging.info(f"Optimized URL for clip {clip}: {optimized_url}")
            print(f"Clip {clip} processed: {optimized_url}")
        else:
            logging.error(f"Skipping optimization for {clip} due to upload failure.")

    logging.info("All clips processed successfully.")

def upload_video_to_cloudinary(video_path):
    logging.info(f"Uploading {video_path} to Cloudinary")
    try:
        upload_result = upload(video_path, resource_type="video", public_id=os.path.basename(video_path))
        video_url = upload_result["secure_url"]
        logging.info(f"Video uploaded to {video_url}")
        return video_url
    except Exception as e:
        logging.error(f"Failed to upload {video_path}: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: python main.py <path_to_video>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    if not os.path.isfile(video_path):
        logging.error(f"Video file not found: {video_path}")
        sys.exit(1)
    
    os.makedirs("clips", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    clips = generate_cuts(video_path)

    if clips:
        process_clips(clips)
    else:
        logging.error("No clips generated, exiting.")

    logging.info("Video processing pipeline completed successfully.")

if __name__ == "__main__":
    main()
