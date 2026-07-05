"""
prompts package
----------------
This package holds one module per persona. Each module must define:

    DISPLAY_NAME : str   -> Human readable name shown in the Streamlit dropdown
    SYSTEM_PROMPT : str  -> The system prompt used to guide Gemini's behavior

To add a NEW persona in the future:
    1. Create a new file, e.g. prompts/career_advisor.py
    2. Define DISPLAY_NAME and SYSTEM_PROMPT inside it
    3. Import it below and add it to the PERSONA_MODULES list

No other part of the application needs to change - the persona will automatically
show up in the sidebar dropdown and get its own independent chat history.
"""

from prompts import farmer
from prompts import teacher
from prompts import coding_assistant
from prompts import interviewer
from prompts import general_assistant

# Register every persona module here. Adding a new persona later is as simple
# as importing it above and appending it to this list.
PERSONA_MODULES = [
    farmer,
    teacher,
    coding_assistant,
    interviewer,
    general_assistant,
]

# Build a lookup dict: { "Expert Farmer": "You are an Expert Farmer...", ... }
PERSONA_PROMPTS = {
    module.DISPLAY_NAME: module.SYSTEM_PROMPT for module in PERSONA_MODULES
}
