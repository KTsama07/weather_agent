# Weather Agent

This repository contains a small Google ADK-based weather assistant with a Streamlit chat UI and an MCP weather tool backend.

## Repository layout

- `/home/runner/work/weather_agent/weather_agent/app.py`  
  Top-level Streamlit entrypoint that imports `agent.app`.

- `/home/runner/work/weather_agent/weather_agent/agent/agent.py`  
  Defines `root_agent` using `google.adk.agents.llm_agent.Agent` with a weather-focused instruction and one MCP toolset.

- `/home/runner/work/weather_agent/weather_agent/agent/mcptools.py`  
  Configures `weather_mcp_tool` via `McpToolset` and launches `@dangahagan/weather-mcp` through `npx` (stdio transport), with metric units and all tools enabled.

- `/home/runner/work/weather_agent/weather_agent/agent/app.py`  
  Main Streamlit app:
  - sets up chat history and a per-session UUID in `st.session_state`
  - creates an `InMemoryRunner` for `root_agent`
  - ensures an ADK session exists
  - sends user messages as `types.Content`
  - streams and renders the agent response in chat UI

- `/home/runner/work/weather_agent/weather_agent/agent/__init__.py`  
  Re-exports `root_agent`.

## How it works

1. Streamlit receives a user prompt.
2. The app ensures an ADK session exists for the current Streamlit session.
3. The prompt is sent to `root_agent` via `InMemoryRunner.run_async(...)`.
4. `root_agent` can call `weather_mcp_tool`.
5. The MCP tool talks to the weather MCP server process (`npx @dangahagan/weather-mcp@latest`) and returns weather data.
6. The response is streamed back into the Streamlit chat.

## Prerequisites

- Python 3.10+
- Node.js + `npx` (required for the MCP weather server)
- Access to Google ADK-compatible model credentials in your environment

## Environment

`agent/agent.py` loads environment variables from:

- `/home/runner/work/weather_agent/weather_agent/agent/.env`

This file is gitignored.

## Run locally

From `/home/runner/work/weather_agent/weather_agent`:

```bash
streamlit run app.py
```

Then open the local Streamlit URL and ask weather questions (for example, “What’s the weather in Tokyo?”).
