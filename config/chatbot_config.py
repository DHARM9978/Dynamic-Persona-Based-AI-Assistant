"""
chatbot_config.py
------------------
Central configuration for PersonaFlow AI.

This module is the single source of truth for:
- Which personas are available (auto-loaded from the prompts package)
- Which Gemini model to use
- Memory / history limits
- App-level constants (title, default persona, etc.)

Keeping all configuration here makes it easy to tweak behavior without
touching business logic elsewhere in the app.
"""

from prompts import PERSONA_PROMPTS

# ---------------------------------------------------------------------------
# App-level constants
# ---------------------------------------------------------------------------
APP_TITLE = "PersonaFlow AI"
APP_SUBTITLE = "Multi-Persona Conversational AI System"

# ---------------------------------------------------------------------------
# Persona configuration (auto-loaded from prompts/__init__.py)
# ---------------------------------------------------------------------------
AVAILABLE_PERSONAS = list(PERSONA_PROMPTS.keys())
DEFAULT_PERSONA = AVAILABLE_PERSONAS[0] if AVAILABLE_PERSONAS else None


def get_system_prompt(persona_name: str) -> str:
    """
    Return the system prompt for a given persona name.
    Falls back to a generic assistant prompt if the persona is unknown.
    """
    return PERSONA_PROMPTS.get(
        persona_name,
        "You are a helpful AI assistant.",
    )


# ---------------------------------------------------------------------------
# Gemini model configuration
# ---------------------------------------------------------------------------
GEMINI_MODEL_NAME = "gemini-2.5-flash"  # Change to gemini-1.5-pro etc. if needed
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_OUTPUT_TOKENS = 1024

# ---------------------------------------------------------------------------
# Memory configuration
# ---------------------------------------------------------------------------
# Maximum number of messages (user + AI combined) retained per persona.
MAX_HISTORY_MESSAGES = 20
