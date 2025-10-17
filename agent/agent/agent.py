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
    # instruction=prompts.INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="http://localhost:6969/mcp",
            ),
            tool_filter=["summarize_chat_history"],
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
            ],
        ),
    ],
)

# template_agent = LlmAgent(
#     model=LiteLlm(model="ollama_chat/qwen3:8b"),
#     name="ppt_template_agent",
#     description="An agent that can create template file based on transcript",
#     tools=[
#         MCPToolset(
#             connection_params=StreamableHTTPServerParams(
#                 url="http://localhost:6969/mcp",
#             ),
#             tool_filter=["generate_ppt_template"],
#         ),
#     ],
# )

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
        ppt_slides_agent,
        # template_agent,
    ],
)
