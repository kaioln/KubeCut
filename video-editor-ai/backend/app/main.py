from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import uvicorn
import os
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import resize
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"Recebendo arquivo: {file.filename}")

        # Definir formatos de vídeo permitidos
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.mpeg', '.mpg'}
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension not in allowed_extensions:
            logger.error(f"Formato de arquivo inválido: {file_extension}")
            raise HTTPException(status_code=400, detail="O formato de vídeo enviado não é aceito.")
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Arquivo salvo em: {file_path}")
        return {"file_path": file_path}
    except Exception as e:
        logger.error(f"Erro no upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-video/")
async def process_video(request: VideoProcessRequest):
    try:
        video_path = request.video_path
        output_format = request.output_format

        if output_format not in ["tiktok", "youtube"]:
            logger.error(f"Formato de saída inválido: {output_format}")
            raise HTTPException(status_code=400, detail="Formato de saída inválido.")

        output_folder = os.path.join(PROCESSED_FOLDER, os.path.basename(video_path).replace(".mp4", ""))
        os.makedirs(output_folder, exist_ok=True)

        # Gera as cenas de acordo com o conteúdo usando PySceneDetect
        logger.info("Iniciando a detecção de cenas.")
        scenes = detect_scenes(video_path)

        # Corta o vídeo de acordo com as cenas e adiciona legendas personalizadas
        logger.info("Iniciando o processamento dos clipes.")
        process_clips_with_dynamic_captions(video_path, output_folder, scenes, output_format)
        
        return JSONResponse(content={"message": "Processamento de vídeo completo!", "output_folder": output_folder})

    except Exception as e:
        logger.error(f"Erro ao processar o vídeo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar o vídeo: {str(e)}")

def detect_scenes(video_path):
    try:
        from scenedetect import VideoManager, SceneManager
        from scenedetect.detectors import ContentDetector

        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector())
        video_manager.set_downscale_factor()
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list()

        # Convertendo lista de cenas para timestamps
        scenes = [(scene[0].get_seconds(), scene[1].get_seconds()) for scene in scene_list]
        logger.info(f"Cenas detectadas: {scenes}")
        return scenes
    except Exception as e:
        logger.error(f"Erro ao detectar cenas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao detectar cenas: {str(e)}")

def generate_captions(video_path):
    try:
        logger.info(f"Iniciando a geração de legendas para o vídeo: {video_path}")
        model = whisper.load_model("base")  # Assumindo que você está usando o modelo 'base'
        result = model.transcribe(video_path)  # Transcreve o áudio do vídeo
        captions = result["text"]  # Extrai o texto transcrito
        logger.info("Legendas geradas com sucesso.")
        return captions, result['segments']
    except Exception as e:
        logger.error(f"Erro ao gerar legendas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar legendas: {str(e)}")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def process_clips_with_dynamic_captions(video_path, output_folder, scenes, output_format):
    try:
        logger.info("Iniciando o processamento do vídeo.")
        video = VideoFileClip(video_path)
        logger.info("Vídeo carregado: %s", video_path)
        
        captions, segments = generate_captions(video_path)
        logger.info("Legendas geradas com sucesso.")

        for i, (start, end) in enumerate(scenes):
            logger.info("Processando cena %d: %s - %s", i, start, end)
            clip = video.subclip(start, end)

            # Filtrar as legendas que pertencem à cena atual
            scene_captions = [seg for seg in segments if seg['start'] >= start and seg['end'] <= end]
            caption_text = "\n".join([seg['text'] for seg in scene_captions])

            # Criar um TextClip usando a função de personalização
            txt_clip = customize_caption_style(caption_text)

            # Posicionar a legenda e combinar com o vídeo
            txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(clip.duration)
            video_with_captions = CompositeVideoClip([clip, txt_clip])

            # Redimensionar de acordo com a plataforma de destino
            if output_format == "tiktok":
                video_with_captions = video_with_captions.fx(resize, newsize=(1080, 1920))
                logger.info("Redimensionando para TikTok (1080x1920).")
            elif output_format == "youtube":
                video_with_captions = video_with_captions.fx(resize, newsize=(1920, 1080))
                logger.info("Redimensionando para YouTube (1920x1080).")

            # Salvar o vídeo processado
            output_file = os.path.join(output_folder, f"scene_{i}.mp4")
            logger.info("Salvando o vídeo com legendas em %s", output_file)
            video_with_captions.write_videofile(
                output_file,
                codec="libx264",
                audio_codec="aac",
                bitrate="5000k",
                fps=clip.fps
            )
            logger.info("Vídeo salvo com sucesso: %s", output_file)

    except Exception as e:
        logger.error("Erro ao processar os cortes: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao processar os cortes: {str(e)}")

# Palavras-chave usadas em vídeos para chamar atenção
KEYWORDS = [
    "importante", "atenção", "sucesso", "alerta", "incrível", "não perca", 
    "última chance", "confira", "agora", "viral", "melhor", "urgente", "surpresa",
    "exclusivo", "top", "especial", "tendência", "segredo", "dica", "estratégia"
]

def customize_caption_style(caption_text):
    # Define valores padrão para a legenda
    font = "Arial-Bold"
    fontsize = 30
    color = "white"
    stroke_color = "black"
    stroke_width = 2

    # Verifica palavras-chave e ajusta o estilo
    if any(keyword in caption_text.lower() for keyword in KEYWORDS):
        font = "Arial-Bold"
        fontsize = 32
        color = "yellow"

    if "urgente" in caption_text.lower():
        font = "Arial-Bold"
        fontsize = 36
        color = "red"

    # Cria um novo TextClip com os estilos definidos
    txt_clip = TextClip(caption_text, fontsize=fontsize, font=font, color=color, stroke_color=stroke_color, stroke_width=stroke_width)

    return txt_clip

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
