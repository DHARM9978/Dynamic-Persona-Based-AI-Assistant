from google import genai
# from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# Use for the local run
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Use for deployment
client = genai.Client(api_key = st.secrets["GOOGLE_API_KEY"])


for model in client.models.list():
    print(model.name)