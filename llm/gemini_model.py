"""
gemini_model.py
----------------
A reusable, single-initialization wrapper around Google's Gemini model via
LangChain's ChatGoogleGenerativeAI class.

Design notes:
- Implemented as a singleton so the underlying model client is created only
  ONCE per app run, no matter how many times get_gemini_model() is called.
- Reads the API key from the environment (.env via python-dotenv).
- Centralizing this here makes it trivial to swap in another LLM provider in
  the future (see "Future Extensibility" - Multiple LLM providers).
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from config.chatbot_config import (
    GEMINI_MODEL_NAME,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_OUTPUT_TOKENS,
)

# Load variables from .env into the process environment
load_dotenv()


class GeminiModel:
    """
    Singleton wrapper around the Gemini chat model.

    Usage:
        model = GeminiModel.get_instance()
        response = model.invoke([...])
    """

    _instance: ChatGoogleGenerativeAI | None = None

    @classmethod
    def get_instance(cls) -> ChatGoogleGenerativeAI:
        """
        Return the already-initialized Gemini model instance, creating it on
        the very first call.
        """
        if cls._instance is None:
            api_key = os.getenv("GOOGLE_API_KEY")

            if not api_key or api_key == "YOUR_API_KEY":
                raise ValueError(
                    "GOOGLE_API_KEY is not set. Please add a valid Gemini API "
                    "key to your .env file before running the app."
                )

        cls._instance = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_NAME,
            google_api_key=api_key,
            temperature=GEMINI_TEMPERATURE,
        )

        return cls._instance


def get_gemini_model() -> ChatGoogleGenerativeAI:
    """
    Convenience function so other modules don't need to know about the
    GeminiModel class directly.
    """
    return GeminiModel.get_instance()
