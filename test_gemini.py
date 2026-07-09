from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
import os

import streamlit as st

# use for the local run
# load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    
    # Use for local run
    # google_api_key=os.getenv("GOOGLE_API_KEY")

    # Use for the deployment
    google_api_key = st.secrets["GOOGLE_API_KEY"]
)

response = llm.invoke("Say hello")

print(response)
print(response.content)