import streamlit as st
import asyncio
import uuid
from google.adk.runners import InMemoryRunner
from google.genai import types
from agent import root_agent # Import your fully configured ADK agent

USER_ID = "streamlit-user"

st.title("☁️ Weather Assistant")
st.caption("Powered by Google ADK and MCP")

# 1. Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit-session-{uuid.uuid4()}"

if "runner" not in st.session_state:
    st.session_state.runner = InMemoryRunner(agent=root_agent)

# 2. Display existing chat messages on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Async wrapper for the ADK agent
async def ensure_adk_session() -> None:
    runner = st.session_state.runner
    session = await runner.session_service.get_session(
        app_name=runner.app_name,
        user_id=USER_ID,
        session_id=st.session_state.session_id,
    )
    if session is None:
        await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id=USER_ID,
            session_id=st.session_state.session_id,
        )


async def get_agent_response(user_input: str) -> str:
    await ensure_adk_session()

    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    response_text = ""

    async for event in st.session_state.runner.run_async(
        user_id=USER_ID,
        session_id=st.session_state.session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            response_text += "".join(part.text or "" for part in event.content.parts)

    return response_text.strip()

# 4. Handle new user input
if prompt := st.chat_input("What's the weather like in Tokyo?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show assistant message with a loading spinner
    with st.chat_message("assistant"):
        with st.spinner("Checking the weather..."):
            # Execute the async agent block
            response_text = asyncio.run(get_agent_response(prompt))
            st.markdown(response_text)
            
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
