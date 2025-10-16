from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import AutoTokenizer
from optimum.intel.openvino import OVModelForCausalLM
import torch


# Initialize FastAPI app
app = FastAPI(title="OpenVINO Qwen3-1.7B API")

# Load OpenVINO model & tokenizer
model_id = "OpenVINO/qwen3-1.7b-fp16-ov"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = OVModelForCausalLM.from_pretrained(model_id)

# Optional: Set device (OpenVINO backend auto-selects)
device = torch.device("cpu")

# Request schema
class OpenAIChatRequest(BaseModel):
    model: str = model_id
    messages: list
    max_tokens: int = 100
    temperature: float = 0.7


# OpenAI-compatible endpoint
@app.post("/v1/chat/completions")
async def chat_completions(request: OpenAIChatRequest):
    try:
        # Extract user message
        user_message = ""
        for msg in request.messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        if not user_message:
            return JSONResponse(
                status_code=400,
                content={"error": "No user message found"}
            )

        # Tokenize and generate
        inputs = tokenizer(user_message, return_tensors="pt").to(device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Format OpenAI-style response
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


# Simple test endpoint
class LLMRequest(BaseModel):
    message: str
    max_new_tokens: int = 100

@app.post("/generate")
async def generate(req: LLMRequest):
    inputs = tokenizer(req.message, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=req.max_new_tokens)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"input": req.message, "output": text}


# Entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5678)
