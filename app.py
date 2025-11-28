import os
from dotenv import load_dotenv

import streamlit as st
from groq import Groq

from kb import add_pdf_to_kb, add_text_to_kb, query_kb

# ----------------------------
# Load API key and create client
# ----------------------------

# Load .env locally (for running on your laptop)
load_dotenv()

def get_groq_api_key():
    # 1) Streamlit Cloud: read from st.secrets
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    # 2) Local dev: read from environment (.env)
    return os.getenv("GROQ_API_KEY")

GROQ_API_KEY = get_groq_api_key()

if not GROQ_API_KEY:
    st.error("🚨 API key missing! Please set GROQ_API_KEY in Streamlit Secrets or .env")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
