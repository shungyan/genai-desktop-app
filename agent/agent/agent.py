from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.agents import LlmAgent, BaseAgent
from . import prompts

# Define individual agents
greeter = LlmAgent(name="Greeter", model=LiteLlm(model="ollama_chat/qwen3:8b"))

summarizer = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:8b"),
    name="summarizer",
    description="An agent that can summarize chat history",
    instruction=prompts.SUMMARIZER_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="http://localhost:6969/mcp",
            ),
            tool_filter=["summarize_chat_history","fetch_chat_history"],
        ),
    ],
)

video_analyst = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:8b"),
    name="video_analyst",
    description="An agent that can analyze video, don't ask user to upload video",
    instruction=prompts.VIDEO_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="http://localhost:6969/mcp",
            ),
            tool_filter=["analyze_video","check_video"],
        ),
    ],
)

transcribe_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:8b"),
    name="transcribe_agent",
    description="An agent transcribe the video",
    instruction=prompts.TRANSCRIBE_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="http://localhost:6969/mcp",
            ),
            tool_filter=["transcribe","check_video"],
        ),
    ],
)

ppt_slides_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/qwen3:8b"),
    name="ppt_slides_agent",
    description="An agent that can create ppt slides based on key points, only run the sequence once",
    instruction=prompts.PPT_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="http://localhost:6969/mcp",
            ),
            tool_filter=[
                "create_ppt",
                "add_slide",
                "write_text",
                "save_ppt",
                "generate_guideline",
            ],
        ),
    ],
)


# Create parent agent and assign children via sub_agents
root_agent = LlmAgent(
    name="Coordinator",
    model=LiteLlm(model="ollama_chat/qwen3:8b"),
    description="I coordinate greetings and tasks.",
    instruction=prompts.COORDINATOR_INSTRUCTION,
    sub_agents=[  # Assign sub_agents here
        greeter,
        summarizer,
        video_analyst,
        transcribe_agent,
        ppt_slides_agent,
    ],
)
