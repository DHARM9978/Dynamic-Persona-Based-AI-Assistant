
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class GeminiModel:
    _instance = None

    @classmethod
    def get_instance(cls):

        if cls._instance is None:

            api_key = os.getenv("GOOGLE_API_KEY")

            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY is not set in .env file"
                )

            cls._instance = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=api_key,
                temperature=0.7,
            )

        return cls._instance


def get_gemini_model():
    return GeminiModel.get_instance()
