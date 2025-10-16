import grpc
from concurrent import futures
import psycopg2
import chat_pb2
import chat_pb2_grpc
import requests

def create_session():
    url_session = "http://localhost:8000/apps/agent/users/u_123/sessions/s_123"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url_session, headers=headers)
    if response.status_code == 200:
        print(f"Session created successfully.")
    else:
        print(f"Failed to create session. Status code: {response.status_code}, response: {response.text}")


def generate_llm_reply(user_message):
    url= "http://localhost:8000/run"
    headers = {"Content-Type": "application/json"}

    payload = {
        "app_name": "agent",
        "user_id": "u_123",
        "session_id": "s_123",
        "new_message": {
            "role": "user",
            "parts": [
                {"text": user_message}
            ]
        }
    }

    llm_response = requests.post(url, headers=headers, json=payload)

    try:
        return llm_response.json()
    except ValueError:
        return llm_response.text



# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):
        # Save user message
        cursor.execute(
            "INSERT INTO conversations (sender, message) VALUES (%s, %s)",
            ("user", request.message)
        )
        conn.commit()

        # Generate LLM reply
        llm_reply = generate_llm_reply(request.message)
        # Extract only the text part safely
        try:
            llm_reply_text = llm_reply[0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            llm_reply_text = str(llm_reply)

        # Save bot reply
        cursor.execute(
            "INSERT INTO conversations (sender, message) VALUES (%s, %s)",
            ("bot", llm_reply_text)
        )
        conn.commit()

        # Return ChatReply to FastAPI
        return chat_pb2.ChatReply(reply=llm_reply_text)

    def UploadVideo(self, request, context):
        filename = "uploaded_video.mp4"
        try:
            with open(filename, "wb") as f:
                f.write(request.file_content)
            print(f"Video saved as {filename}")
            return chat_pb2.VideoReply(message="Video uploaded successfully")
        except Exception as e:
            print(f"Error saving video: {e}")
            return chat_pb2.VideoReply(message=f"Error: {str(e)}")

    def GetHistory(self, request, context):
        cursor.execute(
            "SELECT sender, message, created_at FROM conversations ORDER BY created_at"
        )
        rows = cursor.fetchall()

        messages = [
            chat_pb2.ChatMessage(
                sender=row[0],
                message=row[1],
                created_at=row[2].strftime("%Y-%m-%d %H:%M:%S")
            )
            for row in rows
        ]

        return chat_pb2.ChatHistory(messages=messages)
    
def serve():
    create_session()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 150 * 1024 * 1024),  # 150MB
            ('grpc.max_receive_message_length', 150 * 1024 * 1024),  # 150MB
        ]
    )
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC backend running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
