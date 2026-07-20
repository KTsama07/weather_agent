from pathlib import Path

from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

try:
    from .mcptools import weather_mcp_tool
except ImportError:
    from mcptools import weather_mcp_tool

root_agent = Agent(
    model='gemini-3.1-flash-lite',
    name='root_agent',
    description='A weather assistant for providing weather information.',
    instruction='You are a weather assistant. Use the provided tools to fetch weather information for a specified city.',
    tools=[weather_mcp_tool],
)
