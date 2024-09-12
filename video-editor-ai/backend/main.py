from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os
import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips
import random  # Linha removida

app = FastAPI()

# Pastas para armazenar vídeos
UPLOAD_FOLDER = "uploaded_videos"
PROCESSED_FOLDER = "processed_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

class VideoProcessRequest(BaseModel):
    video_path: str
    output_format: str

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-video/")
async def process_video(request: VideoProcessRequest):
    try:
        video_path = request.video_path
        output_format = request.output_format

        if output_format not in ["tiktok", "youtube"]:
            raise HTTPException(status_code=400, detail="Formato de saída inválido.")

        output_path = os.path.join(PROCESSED_FOLDER, os.path.basename(video_path))
        if output_format == "tiktok":
            scenes = generate_tiktok_scenes(video_path)
        elif output_format == "youtube":
            scenes = generate_youtube_scenes(video_path)

        cut_video(video_path, output_path, scenes)
        captions = generate_captions(video_path)

        with open(output_path.replace(".mp4", ".srt"), "w") as f:
            f.write(captions)

        return JSONResponse(content={"message": "Processamento de vídeo completo!", "output_path": output_path})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_tiktok_scenes(video_path):
    video = VideoFileClip(video_path)
    duration = video.duration
    return [(i, min(i + 15, duration)) for i in range(0, int(duration), 15)]

def generate_youtube_scenes(video_path):
    video = VideoFileClip(video_path)
    duration = video.duration
    return [(i, min(i + 60, duration)) for i in range(0, int(duration), 60)]

def generate_captions(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    captions = result['text']
    return captions

def cut_video(video_path, output_path, scenes):
    try:
        video = VideoFileClip(video_path)
        clips = [video.subclip(scene[0], scene[1]) for scene in scenes]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_path, codec="libx264")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
