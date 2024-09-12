from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os
import whisper

app = FastAPI()

UPLOAD_FOLDER = "uploaded_videos"
PROCESSED_FOLDER = "processed_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

class VideoProcessRequest(BaseModel):
    video_path: str
    output_format: str

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_path": file_path}

@app.post("/process-video/")
async def process_video(request: VideoProcessRequest):
    video_path = request.video_path
    output_format = request.output_format

    captions = generate_captions(video_path)
    output_path = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(video_path)}")
    cut_video(video_path, output_path, [(0, 5), (10, 15)])
    subtitled_output_path = add_subtitles(output_path, captions)
    
    return JSONResponse(content={"message": "Processamento de vídeo completo!", "output_path": subtitled_output_path})

def generate_captions(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    captions = result['text']
    return captions

def cut_video(video_path, output_path, scenes):
    video = VideoFileClip(video_path)
    clips = [video.subclip(scene[0], scene[1]) for scene in scenes]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264")

def add_subtitles(video_path, subtitles):
    video = VideoFileClip(video_path)
    txt_clip = TextClip(subtitles, fontsize=24, color='white', size=video.size)
    txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(video.duration)
    video_with_subtitles = CompositeVideoClip([video, txt_clip])
    subtitled_output_path = video_path.replace("processed_", "subtitled_")
    video_with_subtitles.write_videofile(subtitled_output_path, codec="libx264")
    return subtitled_output_path

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)