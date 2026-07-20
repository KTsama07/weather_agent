import os
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters

weather_mcp_tool = McpToolset(
    connection_params= StdioConnectionParams(
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@dangahagan/weather-mcp@latest"],
            env={
                **os.environ,
                "ENABLED_TOOLS": "all",
                "WEATHER_UNITS": "metric",
            },
        ),
        timeout=30,
    )
)
