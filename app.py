import os
from dotenv import load_dotenv

import streamlit as st
from groq import Groq

from kb import add_pdf_to_kb, add_text_to_kb, query_kb

# ----------------------------
# Load API key safely for Streamlit Cloud
# ----------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY"))

if not GROQ_API_KEY:
    st.error("🚨 API key missing! Please add GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
