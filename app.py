"""
app.py
------
PersonaFlow AI - Multi-Persona Conversational AI System

This is the main Streamlit entry point. It wires together:
    - config.chatbot_config   -> persona list & app settings
    - memory.chat_memory      -> per-persona chat history (Streamlit session_state)
    - chains.chatbot_chain    -> LangChain pipeline that talks to Gemini
    - utils.helpers           -> small UI helper utilities

Run with:
    streamlit run app.py
"""

import streamlit as st

from config.chatbot_config import (
    APP_TITLE,
    APP_SUBTITLE,
    AVAILABLE_PERSONAS,
    DEFAULT_PERSONA,
    get_system_prompt,
)
from memory.chat_memory import (
    get_history,
    add_message,
    clear_history,
    to_langchain_messages,
)
from chains.chatbot_chain import get_ai_response
from utils.helpers import get_persona_icon, format_error_message


# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = DEFAULT_PERSONA


# ---------------------------------------------------------------------------
# Sidebar - Persona selection
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"## 🧠 {APP_TITLE}")
    st.caption(APP_SUBTITLE)
    st.divider()

    st.markdown("### Select Persona")
    selected_persona = st.selectbox(
        label="Choose an AI expert to chat with:",
        options=AVAILABLE_PERSONAS,
        index=AVAILABLE_PERSONAS.index(st.session_state.selected_persona)
        if st.session_state.selected_persona in AVAILABLE_PERSONAS
        else 0,
        label_visibility="collapsed",
    )
    st.session_state.selected_persona = selected_persona

    icon = get_persona_icon(selected_persona)
    st.info(f"{icon} **Active Persona:** {selected_persona}")

    st.divider()

    if st.button("🗑️ Clear Chat for This Persona", use_container_width=True):
        clear_history(selected_persona)
        st.rerun()

    st.divider()
    st.caption(
        "Each persona keeps its own independent conversation history "
        "(latest 20 messages). Switching personas never mixes chats."
    )


# ---------------------------------------------------------------------------
# Main area - Chat interface
# ---------------------------------------------------------------------------
icon = get_persona_icon(selected_persona)
st.markdown(f"### {icon} Chatting with: **{selected_persona}**")
st.divider()

# Render existing conversation for the currently selected persona
history = get_history(selected_persona)

chat_container = st.container(height=500)
with chat_container:
    if not history:
        st.markdown(
            f"*Say hello to your {selected_persona}! Ask a question to get started.*"
        )
    for message in history:
        avatar = "🧑" if message["role"] == "user" else icon
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Chat input box (pinned at the bottom by Streamlit automatically)
user_input = st.chat_input(f"Message your {selected_persona}...")

if user_input:
    # 1. Save & display the user's message immediately
    add_message(selected_persona, "user", user_input)
    with chat_container:
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

    # 2. Generate the AI response
    with chat_container:
        with st.chat_message(selected_persona, avatar=icon):
            with st.spinner(f"{selected_persona} is thinking..."):
                try:
                    system_prompt = get_system_prompt(selected_persona)
                    # History up to (but not including) the message we just added
                    lc_history = to_langchain_messages(selected_persona)[:-1]

                    ai_response = get_ai_response(
                        system_prompt=system_prompt,
                        history=lc_history,
                        user_input=user_input,
                    )
                    st.markdown(ai_response)
                    add_message(selected_persona, "assistant", ai_response)

                except Exception as error:
                    error_message = format_error_message(error)
                    st.error(error_message)

    st.rerun()
