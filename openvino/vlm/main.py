from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import AutoTokenizer
from optimum.intel.openvino import OVModelForCausalLM
import torch


# Initialize FastAPI app
app = FastAPI(title="OpenVINO VLM API")

# Load OpenVINO model & tokenizer
# model_id = "OpenVINO/qwen3-1.7b-fp16-ov"
model_id = "OpenVINO/Phi-3.5-vision-instruct-fp16-ov"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = OVModelForCausalLM.from_pretrained(model_id)


device = torch.device("cpu")

# Request schema
class OpenAIChatRequest(BaseModel):
    model: str = model_id
    messages: list
    max_tokens: int = 100
    temperature: float = 0.7


# OpenAI-compatible endpoint
@app.post("/v1/chat/completions")
class ChatMessage(BaseModel):
    role: str
    content: str
    images: Optional[str] = None  # base64-encoded image string

class OpenAIChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 256
    stream: Optional[bool] = False


# ----- Endpoint -----
@app.post("/v1/chat/completions")
async def chat_completions(request: OpenAIChatRequest):
    try:
        user_message = ""
        image_data = None

        # Extract user text and optional image
        for msg in request.messages:
            if msg.role == "user":
                user_message = msg.content
                if msg.images:
                    # Decode base64 → image
                    image_bytes = base64.b64decode(msg.images)
                    image_data = Image.open(BytesIO(image_bytes))
                break

        if not user_message and not image_data:
            return JSONResponse(
                status_code=400,
                content={"error": "No user message or image found"}
            )

        # ----- Model Inference -----
        if image_data:
            # VLM: process both image and text
            inputs = processor(images=image_data, text=user_message, return_tensors="pt").to(device)
            outputs = model.generate(**inputs, max_new_tokens=request.max_tokens, temperature=request.temperature)
        else:
            # Text-only model
            inputs = tokenizer(user_message, return_tensors="pt").to(device)
            outputs = model.generate(**inputs, max_new_tokens=request.max_tokens, temperature=request.temperature)

        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # ----- OpenAI-style Response -----
        response = {
            "id": "chatcmpl-001",
            "object": "chat.completion",
            "created": 1677652288,
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(inputs["input_ids"][0]),
                "completion_tokens": len(outputs[0]),
                "total_tokens": len(inputs["input_ids"][0]) + len(outputs[0])
            }
        }

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# Entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
