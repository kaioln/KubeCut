from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import uvicorn
import os
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import resize
import scenedetect
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import numpy as np

app = FastAPI()

UPLOAD_FOLDER = "uploaded_videos"
PROCESSED_FOLDER = "processed_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

class VideoProcessRequest(BaseModel):
    video_path: str
    output_format: str

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="O arquivo enviado não é um vídeo.")
        
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

        output_folder = os.path.join(PROCESSED_FOLDER, os.path.basename(video_path).replace(".mp4", ""))
        os.makedirs(output_folder, exist_ok=True)

        # Gera as cenas de acordo com o conteúdo usando PySceneDetect
        scenes = detect_scenes(video_path)

        # Corta o vídeo de acordo com as cenas e adiciona legendas personalizadas
        process_clips_with_dynamic_captions(video_path, output_folder, scenes, output_format)
        
        return JSONResponse(content={"message": "Processamento de vídeo completo!", "output_folder": output_folder})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o vídeo: {str(e)}")

def detect_scenes(video_path):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    # Convertendo lista de cenas para timestamps
    scenes = [(scene[0].get_seconds(), scene[1].get_seconds()) for scene in scene_list]
    return scenes

def generate_captions(video_path):
    model = whisper.load_model("base")  # Assumindo que você está usando o modelo 'base'
    result = model.transcribe(video_path)  # Transcreve o áudio do vídeo
    captions = result["text"]  # Extrai o texto transcrito
    return captions

def format_captions(segments):
    captions = []
    for i, segment in enumerate(segments):
        start = segment['start']
        end = segment['end']
        text = segment['text']
        captions.append(f"{i+1}\n{format_time(start)} --> {format_time(end)}\n{text}\n")
    return "\n".join(captions)

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def process_clips_with_dynamic_captions(video_path, output_folder, scenes, output_format):
    try:
        video = VideoFileClip(video_path)
        captions, segments = generate_captions(video_path)

        for i, (start, end) in enumerate(scenes):
            clip = video.subclip(start, end)

            # Determina o estilo das legendas com base no conteúdo e ambientação
            scene_captions = [seg for seg in segments if seg['start'] >= start and seg['end'] <= end]
            caption_text = "\n".join([seg['text'] for seg in scene_captions])
            
            txt_clip = TextClip(caption_text, fontsize=24, color='white', bg_color='black')
            txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(clip.duration)

            # Personaliza a escala e posição das legendas baseadas no conteúdo da cena
            txt_clip = customize_caption_style(txt_clip, caption_text)

            # Composição do vídeo com legendas
            video_with_captions = CompositeVideoClip([clip, txt_clip])
            
            # Redimensiona o vídeo para a plataforma de saída (TikTok ou YouTube)
            if output_format == "tiktok":
                video_with_captions = video_with_captions.fx(resize, newsize=(1080, 1920))
            elif output_format == "youtube":
                video_with_captions = video_with_captions.fx(resize, newsize=(1920, 1080))

            video_with_captions.write_videofile(
                os.path.join(output_folder, f"scene_{i}.mp4"), codec="libx264"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar os cortes: {str(e)}")

def customize_caption_style(txt_clip, caption_text):
    # Exemplo básico de personalização de estilo de legendas
    if "dark" in caption_text.lower():
        txt_clip = txt_clip.set_color("yellow")
    elif "bright" in caption_text.lower():
        txt_clip = txt_clip.set_color("black")
    # Pode-se adicionar mais lógica para ajustar fonte, tamanho, cor, etc.
    return txt_clip

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
