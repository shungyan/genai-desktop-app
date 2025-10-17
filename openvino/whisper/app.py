from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from moviepy.editor import VideoFileClip
import numpy as np
import soundfile as sf
from pathlib import Path
import tempfile
import os
import librosa

from transformers import AutoProcessor
from optimum.intel.openvino import OVModelForSpeechSeq2Seq
import uvicorn


app = FastAPI(title="Whisper OpenVINO Speech-to-Text API")

MODEL_ID = "OpenVINO/distil-whisper-large-v2-fp16-ov"
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = OVModelForSpeechSeq2Seq.from_pretrained(MODEL_ID)



def extract_audio_from_video(video_path: Path, target_sr: int = 16000) -> dict:
    """Extract and resample audio to 16 kHz mono using librosa."""
    wav_path = video_path.with_suffix(".wav")

    # Extract audio from MP4
    clip = VideoFileClip(str(video_path))
    clip.audio.write_audiofile(str(wav_path), logger=None)
    clip.close()

    # Load and resample using librosa
    audio, sr = librosa.load(str(wav_path), sr=target_sr, mono=True)

    return {"array": audio, "sampling_rate": sr}



@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)

        # Extract and preprocess audio
        sample = extract_audio_from_video(tmp_path)

        # Tokenize
        inputs = processor(
            sample["array"],
            sampling_rate=sample["sampling_rate"],
            return_tensors="pt"
        ).input_features

        # Generate text
        predicted_ids = model.generate(inputs)
        transcription = processor.batch_decode(
            predicted_ids, skip_special_tokens=True
        )[0]

        # Clean up temporary files
        os.remove(tmp_path)
        wav_file = tmp_path.with_suffix(".wav")
        if wav_file.exists():
            os.remove(wav_file)

        return JSONResponse({"transcription": transcription})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=4896, reload=True)
