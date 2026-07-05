"""
chat_memory.py
--------------
Manages per-persona conversation history using Streamlit's session_state.

Each persona gets its own independent list of messages, so switching personas
in the sidebar never mixes conversations.

History is stored as a list of dicts:
    {"role": "user" | "assistant", "content": "<message text>"}

This plain-dict format is easy to render in Streamlit's chat UI, and is
converted to LangChain message objects only when calling the chain
(see chains/chatbot_chain.py).
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from config.chatbot_config import MAX_HISTORY_MESSAGES

SESSION_KEY = "persona_histories"


def _ensure_store_initialized() -> None:
    """Make sure the top-level history container exists in session_state."""
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = {}


def get_history(persona_name: str) -> list[dict]:
    """
    Return the message history (list of dicts) for a given persona.
    Creates an empty history if this persona has not been used yet.
    """
    _ensure_store_initialized()
    return st.session_state[SESSION_KEY].setdefault(persona_name, [])


def add_message(persona_name: str, role: str, content: str) -> None:
    """
    Append a new message to a persona's history and trim it to the
    configured maximum length (keeping the most recent messages).
    """
    history = get_history(persona_name)
    history.append({"role": role, "content": content})

    # Trim oldest messages if we exceed the configured limit.
    if len(history) > MAX_HISTORY_MESSAGES:
        overflow = len(history) - MAX_HISTORY_MESSAGES
        del history[:overflow]


def clear_history(persona_name: str) -> None:
    """Clear the conversation history for a single persona."""
    _ensure_store_initialized()
    st.session_state[SESSION_KEY][persona_name] = []


def to_langchain_messages(persona_name: str) -> list:
    """
    Convert this persona's stored dict-based history into LangChain
    HumanMessage / AIMessage objects, ready to be passed into the chain's
    MessagesPlaceholder.
    """
    history = get_history(persona_name)
    lc_messages = []
    for msg in history:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    return lc_messages
