"""
chatbot_chain.py
-----------------
Builds the LangChain pipeline that powers every persona's conversation.

Conversation Flow:

    System Prompt
        +
    Chat History (MessagesPlaceholder)
        +
    User Input
        |
        v
      Gemini
        |
        v
   AI Response

The same chain structure is reused for every persona - only the
`system_prompt` value that gets passed in at invocation time changes.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from llm.gemini_model import get_gemini_model

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------
# "system_prompt" and "user_input" are filled in dynamically per persona/turn.
# "history" is populated via MessagesPlaceholder with prior HumanMessage /
# AIMessage objects for the currently selected persona.
CHAT_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", "{system_prompt}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_input}"),
    ]
)


def build_chain():
    """
    Build (or rebuild) the full LangChain pipeline:
        prompt_template -> Gemini model -> string output parser

    Because get_gemini_model() returns a singleton, calling this function
    multiple times does NOT re-initialize the underlying Gemini client.
    """
    model = get_gemini_model()
    return CHAT_PROMPT_TEMPLATE | model | StrOutputParser()


def get_ai_response(system_prompt: str, history: list, user_input: str) -> str:
    """
    Run the chain for a single conversational turn.

    Args:
        system_prompt: The persona's system prompt.
        history: List of LangChain HumanMessage/AIMessage objects (prior turns).
        user_input: The latest message typed by the user.

    Returns:
        The model's text response as a plain string.
    """
    chain = build_chain()
    response = chain.invoke(
        {
            "system_prompt": system_prompt,
            "history": history,
            "user_input": user_input,
        }
    )
    print("RESPONSE:", repr(response))
    return response
