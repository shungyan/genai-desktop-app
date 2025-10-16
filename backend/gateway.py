from fastapi import FastAPI, UploadFile, File
import grpc
import chat_pb2, chat_pb2_grpc
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat_endpoint(data: dict):
    message = data.get("message", "")
    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    response = stub.SendMessage(chat_pb2.ChatRequest(message=message))
    return {"reply": response.reply}

@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    file_content = await file.read()
    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    response = stub.UploadVideo(
        chat_pb2.VideoRequest(file_content=file_content, filename=file.filename)
    )

    return {"message": response.message}

@app.get("/history")
async def get_chat_history():
    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    response = stub.GetHistory(chat_pb2.Empty())
    return {"messages": [
        {"sender": msg.sender, "message": msg.message, "created_at": msg.created_at}
        for msg in response.messages
    ]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1234)
# To run: uvicorn gateway:app --reload --host 0.0.0.0 --port 1234
