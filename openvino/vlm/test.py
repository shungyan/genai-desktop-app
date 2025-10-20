import requests
import cv2

def extract_key_frame(video_path, interval_sec=3, max_frames=20):
    """Extract several frames every few seconds."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps == 0 or total_frames == 0:
        raise ValueError(
            f"Invalid video properties: fps={fps}, total_frames={total_frames}"
        )
    duration = total_frames / fps

    frames_b64 = []
    timestamps = np.arange(0, duration, interval_sec)

    for t in timestamps[:max_frames]:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        frames_b64.append(base64.b64encode(buffer).decode("utf-8"))

    cap.release()
    return frames_b64

video_path = "../../backend/uploaded_video.mp4"

print("extracting....")
image_b64 = extract_key_frame(video_path)
print("done")

# Ollama API endpoint
url = "http://localhost:8765/v1/chat/completions"
question = "summarize this image"

# Prepare request payload
payload = {
    "model": "minicpm-v",
    "messages": [
        {
            "role": "user",
            "content": question,
            "images": image_b64,
        },
    ],
    "stream": False,
}

# Send request
response = requests.post(url, json=payload, stream=False)
if response.status_code != 200:
    raise RuntimeError(f"API error: {response.text}")

result = response.json()["message"]["content"]

print(result)