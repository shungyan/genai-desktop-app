from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# Allow frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_PATH = "uploaded_video.mp4"

@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    # Remove old video if exists
    if os.path.exists(UPLOAD_PATH):
        os.remove(UPLOAD_PATH)

    # Save new video
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Video '{file.filename}' saved successfully as '{UPLOAD_PATH}'."}
