# Importa as bibliotecas necessárias
from fastapi import FastAPI, UploadFile, File, HTTPException  # FastAPI para construir a API, UploadFile e File para upload de arquivos, HTTPException para erros HTTP
from fastapi.responses import JSONResponse  # Para retornar respostas JSON personalizadas
from pydantic import BaseModel  # Para definir modelos de dados que são validados automaticamente
import shutil  # Para operações de arquivo, como mover ou copiar arquivos
import uvicorn  # Importa o Uvicorn para rodar o servidor ASGI
import os  # Para operações de sistema como criar pastas
import whisper  # Biblioteca Whisper da OpenAI para reconhecimento de fala
from moviepy.editor import VideoFileClip, concatenate_videoclips  # MoviePy para manipulação e edição de vídeo

app = FastAPI()

# Define pastas para armazenar vídeos carregados e processados
UPLOAD_FOLDER = "uploaded_videos"
PROCESSED_FOLDER = "processed_videos"
# Cria as pastas se elas não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Modelo de dados para a requisição de processamento de vídeo
class VideoProcessRequest(BaseModel):
    video_path: str  # Caminho do vídeo a ser processado
    output_format: str  # Formato de saída (tiktok ou youtube)

# Rota de teste para verificar se o servidor está rodando
@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

# Endpoint para upload de vídeo
@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Verifica se o arquivo enviado é um vídeo
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="O arquivo enviado não é um vídeo.")
        
        # Salva o arquivo de vídeo na pasta de upload
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)  # Copia o conteúdo do arquivo enviado para o local de destino
        
        return {"file_path": file_path}  # Retorna o caminho do arquivo carregado
    except Exception as e:
        # Lida com erros inesperados e retorna um erro HTTP
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para processar o vídeo de acordo com o formato especificado (TikTok ou YouTube)
@app.post("/process-video/")
async def process_video(request: VideoProcessRequest):
    try:
        # Extrai o caminho do vídeo e o formato de saída da requisição
        video_path = request.video_path
        output_format = request.output_format

        # Verifica se o formato de saída é válido
        if output_format not in ["tiktok", "youtube"]:
            raise HTTPException(status_code=400, detail="Formato de saída inválido.")

        # Define o caminho de saída para o vídeo processado
        output_path = os.path.join(PROCESSED_FOLDER, os.path.basename(video_path))

        # Gera as cenas de acordo com o formato especificado
        if output_format == "tiktok":
            scenes = generate_tiktok_scenes(video_path)
        elif output_format == "youtube":
            scenes = generate_youtube_scenes(video_path)

        # Corta o vídeo de acordo com as cenas geradas
        cut_video(video_path, output_path, scenes)
        
        # Gera legendas para o vídeo usando o modelo Whisper
        captions = generate_captions(video_path)

        # Salva as legendas geradas em um arquivo .srt
        with open(output_path.replace(".mp4", ".srt"), "w") as f:
            f.write(captions)

        # Retorna uma resposta indicando que o processamento foi concluído
        return JSONResponse(content={"message": "Processamento de vídeo completo!", "output_path": output_path})

    except Exception as e:
        # Lida com erros inesperados e retorna um erro HTTP
        raise HTTPException(status_code=500, detail=str(e))

# Função para gerar cenas de vídeo para o formato TikTok (clips de 15 segundos)
def generate_tiktok_scenes(video_path):
    video = VideoFileClip(video_path)  # Carrega o vídeo usando MoviePy
    duration = video.duration  # Obtém a duração do vídeo em segundos
    # Divide o vídeo em cenas de 15 segundos
    return [(i, min(i + 15, duration)) for i in range(0, int(duration), 15)]

# Função para gerar cenas de vídeo para o formato YouTube (clips de 60 segundos)
def generate_youtube_scenes(video_path):
    video = VideoFileClip(video_path)  # Carrega o vídeo usando MoviePy
    duration = video.duration  # Obtém a duração do vídeo em segundos
    # Divide o vídeo em cenas de 60 segundos
    return [(i, min(i + 60, duration)) for i in range(0, int(duration), 60)]

# Função para gerar legendas para o vídeo usando o modelo Whisper
def generate_captions(video_path):
    model = whisper.load_model("base")  # Carrega o modelo Whisper
    result = model.transcribe(video_path)  # Transcreve o áudio do vídeo
    captions = result['text']  # Extrai o texto transcrito
    return captions

# Função para cortar o vídeo com base nas cenas fornecidas e salvar o vídeo processado
def cut_video(video_path, output_path, scenes):
    try:
        video = VideoFileClip(video_path)  # Carrega o vídeo usando MoviePy
        # Cria uma lista de clips a partir das cenas fornecidas
        clips = [video.subclip(scene[0], scene[1]) for scene in scenes]
        # Concatena os clips em um único vídeo
        final_clip = concatenate_videoclips(clips)
        # Salva o vídeo final no caminho de saída especificado
        final_clip.write_videofile(output_path, codec="libx264")
    except Exception as e:
        # Lida com erros inesperados e retorna um erro HTTP
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Inicia o servidor na porta 8001
