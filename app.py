import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

from kb import add_pdf_to_kb, add_text_to_kb, query_kb

# ===============================
# Load API key (works on Cloud + Local)
# ===============================

def get_groq_api_key():
    # 1) Streamlit Cloud → st.secrets
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]

    # 2) Local machine → .env
    load_dotenv()
    return os.getenv("GROQ_API_KEY")


GROQ_API_KEY = get_groq_api_key()

if not GROQ_API_KEY:
    st.error("🚨 API key missing! Please add GROQ_API_KEY in Streamlit Secrets or .env")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ===============================
# Helper Functions
# ===============================

def build_prompt(question: str, contexts):
    if contexts:
        context_blocks = []
        for c in contexts:
            context_blocks.append(
                f"Source: {c['source']}\nContent: {c['text']}"
            )
        context_text = "\n\n---\n\n".join(context_blocks)
    else:
        context_text = "No relevant documents found."

    return f"""
You are a Knowledge Base Assistant.

- Answer ONLY using the provided context.
- If answer is missing, say “I don’t know”.
- End with a short list of used sources.

Context:
{context_text}

Question: {question}
"""


def answer_question(question: str):
    ctx = query_kb(question, k=4)
    prompt = build_prompt(question, ctx)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You answer strictly using context."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    return completion.choices[0].message.content, ctx

# ===============================
# Streamlit UI
# ===============================

def main():
    st.set_page_config(page_title="Knowledge Agent", page_icon="📚")
    st.title("📚 Company Knowledge Base Agent")

    st.sidebar.header("Upload Documents")

    uploaded_files = st.sidebar.file_uploader(
        "Upload PDFs or Text files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if st.sidebar.button("Add to Knowledge Base") and uploaded_files:
        os.makedirs("temp_files", exist_ok=True)
        total_chunks = 0

        with st.spinner("Processing files..."):
            for f in uploaded_files:
                temp_path = f"temp_files/{f.name}"
                with open(temp_path, "wb") as tmp:
                    tmp.write(f.read())

                if f.name.lower().endswith(".pdf"):
                    chunks = add_pdf_to_kb(temp_path, f.name)
                else:
                    text = open(temp_path, "r", errors="ignore").read()
                    chunks = add_text_to_kb(text, f.name)

                total_chunks += chunks

        st.sidebar.success(f"Added {len(uploaded_files)} file(s) → {total_chunks} chunks")

    # Chat UI
    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_q = st.text_input("Ask a question from your documents:")

    if st.button("Ask") and user_q.strip():
        with st.spinner("Thinking..."):
            try:
                ans, ctx = answer_question(user_q)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        st.session_state.chat.append(("You", user_q))
        st.session_state.chat.append(("Agent", ans))

    # Display chat history
    for role, content in st.session_state.chat:
        st.markdown(f"**{role}:** {content}")

    st.caption("Built using Groq + ChromaDB + Streamlit")

if __name__ == "__main__":
    main()
