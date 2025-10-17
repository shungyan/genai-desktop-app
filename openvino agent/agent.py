from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
        model="openai/Qwen3-1.7B-fp16-ov",
        api_base="http://localhost:5678/v1",
        api_key="none",
)

root_agent = LlmAgent(
    model=model,
    name='ai_agent',
    description='A helpful assistant that answers questions',
    # Add tools if needed
)