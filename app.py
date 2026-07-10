
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


# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
)

# ------------------------------------------------------------------
# SESSION INITIALIZATION
# ------------------------------------------------------------------
if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = DEFAULT_PERSONA

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"## 🧠 {APP_TITLE}")
    st.caption(APP_SUBTITLE)
    st.divider()

    selected_persona = st.selectbox(
        "Choose Persona",
        AVAILABLE_PERSONAS,
        index=AVAILABLE_PERSONAS.index(
            st.session_state.selected_persona
        ),
    )

    st.session_state.selected_persona = selected_persona

    icon = get_persona_icon(selected_persona)

    st.info(
        f"{icon} Active Persona: {selected_persona}"
    )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):
        clear_history(selected_persona)
        st.rerun()

# ------------------------------------------------------------------
# MAIN CHAT AREA
# ------------------------------------------------------------------
icon = get_persona_icon(selected_persona)

st.title(APP_TITLE)

st.markdown(
    f"### {icon} Chatting with **{selected_persona}**"
)

history = get_history(selected_persona)

# ------------------------------------------------------------------
# DISPLAY CHAT HISTORY
# ------------------------------------------------------------------
for message in history:

    avatar = (
        "🧑"
        if message["role"] == "user"
        else icon
    )

    role = (
        "user"
        if message["role"] == "user"
        else "assistant"
    )

    with st.chat_message(
        role,
        avatar=avatar,
    ):
        st.markdown(message["content"])

# ------------------------------------------------------------------
# USER INPUT
# ------------------------------------------------------------------
user_input = st.chat_input(
    f"Message your {selected_persona}..."
)

if user_input:

    # Show user message immediately
    with st.chat_message(
        "user",
        avatar="🧑",
    ):
        st.markdown(user_input)

    try:

        system_prompt = get_system_prompt(
            selected_persona
        )

        # Existing history only
        lc_history = to_langchain_messages(
            selected_persona
        )

        print("=" * 50)
        print("PERSONA:", selected_persona)
        print("HISTORY COUNT:", len(lc_history))
        print("USER INPUT:", user_input)

        with st.chat_message(
            "assistant",
            avatar=icon,
        ):
            with st.spinner(
                f"{selected_persona} is thinking..."
            ):

                ai_response = get_ai_response(
                    system_prompt=system_prompt,
                    history=lc_history,
                    user_input=user_input,
                )

                print(
                    "AI RESPONSE:",
                    repr(ai_response),
                )

                st.markdown(ai_response)

        # Save AFTER successful response
        add_message(
            selected_persona,
            "user",
            user_input,
        )

        add_message(
            selected_persona,
            "assistant",
            ai_response,
        )

    except Exception as error:

        import traceback

        st.exception(error)

        st.code(traceback.format_exc())

    st.rerun()
