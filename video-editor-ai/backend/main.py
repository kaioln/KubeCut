from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "uploaded_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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


    return JSONResponse(content={"message": "Processamento de vídeo completo!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
