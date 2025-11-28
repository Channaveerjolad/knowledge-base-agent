import os
from dotenv import load_dotenv

import streamlit as st
from groq import Groq

from kb import add_pdf_to_kb, add_text_to_kb, query_kb

# ----------------------------
# Load API key (works on Streamlit Cloud and locally)
# ----------------------------

load_dotenv()  # for local .env use


def get_groq_api_key():
    # 1) Streamlit Cloud: read from st.secrets
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        # st.secrets doesn't exist when running plain "python app.py"
        pass

    # 2) Local dev: read from environment (.env loaded above)
    return os.getenv("GROQ_API_KEY")


GROQ_API_KEY = get_groq_api_key()

if not GROQ_API_KEY:
    st.error("🚨 API key missing! Please set GROQ_API_KEY in Streamlit Secrets or .env")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
