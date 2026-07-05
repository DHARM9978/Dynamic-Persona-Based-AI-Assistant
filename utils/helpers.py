"""
helpers.py
----------
Small, generic utility functions shared across the app.
Keeping these separate from app.py keeps the main Streamlit file focused on
UI/layout instead of business logic.
"""

# Simple mapping of persona -> emoji, used purely for a nicer UI.
# Add an entry here whenever a new persona is added for a matching icon,
# otherwise a default icon is used automatically.
PERSONA_ICONS = {
    "Expert Farmer": "🌾",
    "High School Teacher": "🍎",
    "Coding Assistant": "💻",
    "Interview Coach": "🎤",
    "Career Advisor": "🧭",
    "General Assistant": "🤖",
}

DEFAULT_ICON = "🧠"


def get_persona_icon(persona_name: str) -> str:
    """Return a display icon/emoji for a given persona name."""
    return PERSONA_ICONS.get(persona_name, DEFAULT_ICON)


def format_error_message(error: Exception) -> str:
    """
    Convert a raw exception into a clean, user-friendly error string to show
    in the Streamlit UI (instead of a raw stack trace).
    """
    error_text = str(error)

    if "API_KEY" in error_text.upper() or "GOOGLE_API_KEY" in error_text.upper():
        return (
            "⚠️ Gemini API key issue. Please check that a valid GOOGLE_API_KEY "
            "is set in your `.env` file."
        )

    if "quota" in error_text.lower() or "rate" in error_text.lower():
        return (
            "⚠️ The Gemini API rate limit or quota was exceeded. "
            "Please wait a moment and try again."
        )

    return f"⚠️ Something went wrong while generating a response: {error_text}"
