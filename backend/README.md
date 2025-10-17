# 🧱 Step 1: Create a clean project folder

```
mkdir grpc
cd grpc
```

---
# 🧩 Step 2: uv pip install dependencies 
  
  If you’re using **uv** (recommended):
  
  ```
  uv venv
  uv pip install grpcio grpcio-tools uvicorn fastapi
  ```
# 📜 Step 3: Create your  `.proto`  file
  
  In the root folder, create:
  
  ```
  chat.proto
  ```
  
  and put this inside:
  
  ```
  syntax = "proto3";
  
  package chat;
  
  // The service definition (like a REST controller)
  service ChatService {
  rpc SendMessage (ChatRequest) returns (ChatReply);
  }
  
  // The request structure
  message ChatRequest {
  string message = 1;
  }
  
  // The response structure
  message ChatReply {
  string reply = 1;
  }
  ```
  
  This defines your API “contract” — one RPC method called `SendMessage()`.
  
  ---
# ⚙️ Step 4: Generate the Python gRPC code
  
  Run this:
  
  ```
  uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
  ```
  
  ✅ This creates:
  
  ```
  chat_pb2.py
  chat_pb2_grpc.py
  ```
  
  ---
# 🧠 Step 5: Create the gRPC  **server**
  
  File: `server.py`
  
  ```
  import grpc
  from concurrent import futures
  import chat_pb2, chat_pb2_grpc
  
  class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):
        print(f"User said: {request.message}")
        return chat_pb2.ChatReply(reply=f"You said: {request.message}")
  
  def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("✅ gRPC server started on port 50051")
    server.wait_for_termination()
  
  if __name__ == "__main__":
    serve()
  ```
  
  Run it:
  
  ```
  python server.py
  ```
  
  ---
# 🧩 Step 6: Connect to FastAPI
  
  You can now use this same gRPC client inside a FastAPI endpoint, like:
  
  ```
  from fastapi import FastAPI
  import grpc
  import chat_pb2, chat_pb2_grpc
  
  app = FastAPI()
  
  @app.post("/chat")
  def chat(data: dict):
    message = data["message"]
  
    channel = grpc.insecure_channel("localhost:50051")
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    response = stub.SendMessage(chat_pb2.ChatRequest(message=message))
  
    return {"reply": response.reply}
  ```
  
  ---
- # ✅ Summary of File Structure
  
  ```
  grpc-demo/
  ├── chat.proto
  ├── chat_pb2.py
  ├── chat_pb2_grpc.py
  ├── server.py
  └── gateway.py
  ```
