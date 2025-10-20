# How to test OpenVINO LLM

LLM
```bash
curl -X POST http://localhost:5678/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"OpenVINO/qwen3-8b-fp16-ov\",\"messages\":[{\"role\":\"system\",\"content\":\"You are a helpful assistant.\"},{\"role\":\"user\",\"content\":\"Explain quantum computing in simple terms.\"}],\"temperature\":0.7,\"max_tokens\":200}"
```

