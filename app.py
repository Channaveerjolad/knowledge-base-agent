import os
from dotenv import load_dotenv

import streamlit as st
from groq import Groq

from kb import add_pdf_to_kb, add_text_to_kb, query_kb

# ----------------------------
# Load API key and create client
# ----------------------------

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Please put it in your .env file like:\n"
        "GROQ_API_KEY=your_key_here"
    )

client = Groq(api_key=GROQ_API_KEY)


# ----------------------------
# Helper functions
# ----------------------------

def build_prompt(question: str, contexts):
    """
    Construct the prompt for Llama 3 using retrieved knowledge base chunks.
    """
    if contexts:
        context_texts = []
        for c in contexts:
            context_texts.append(f"Source: {c['source']}\nContent: {c['text']}")
        context_block = "\n\n---\n\n".join(context_texts)
    else:
        context_block = "No relevant documents were found in the knowledge base."

    prompt = f"""
You are an AI Knowledge Base Assistant for a company.

You MUST:
- Answer ONLY using the information from the context documents.
- If the answer is not in the documents, clearly say you don't know.
- At the end, briefly list which sources you used.

Context documents:
{context_block}

User question: {question}

Now provide a helpful, concise answer in 4–8 lines.
"""
    return prompt


def answer_question(question: str):
    """
    Retrieve relevant context from KB and ask Groq Llama 3 for an answer.
    """
    contexts = query_kb(question, k=4)
    prompt = build_prompt(question, contexts)

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a strict, factual company knowledge base assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
    )

    answer = chat_completion.choices[0].message.content
    return answer, contexts


# ----------------------------
# Streamlit UI
# ----------------------------

def main():
    st.set_page_config(page_title="Knowledge Base Agent", page_icon="📚")
    st.title("📚 Company Knowledge Base Agent")
    st.write("Ask any question based on the uploaded company documents.")

    # Sidebar – file upload
    st.sidebar.header("Upload Documents")

    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF or text files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

    if st.sidebar.button("Add to Knowledge Base") and uploaded_files:
        with st.spinner("Processing and indexing documents..."):
            total_chunks = 0
            os.makedirs("temp_files", exist_ok=True)

            for f in uploaded_files:
                temp_path = os.path.join("temp_files", f.name)
                with open(temp_path, "wb") as tmp:
                    tmp.write(f.read())

                if f.name.lower().endswith(".pdf"):
                    chunks = add_pdf_to_kb(temp_path, f.name)
                else:
                    with open(
                        temp_path, "r", encoding="utf-8", errors="ignore"
                    ) as txt_file:
                        text = txt_file.read()
                    chunks = add_text_to_kb(text, f.name)

                total_chunks += chunks

            st.sidebar.success(
                f"Added {len(uploaded_files)} file(s) "
                f"({total_chunks} text chunk(s)) to Knowledge Base."
            )

    # Chat UI
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Your question")

    if st.button("Ask") and user_question.strip():
        with st.spinner("Thinking..."):
            try:
                answer, contexts = answer_question(user_question.strip())
            except Exception as e:
                st.error(f"Error while answering: {e}")
                answer = None

        if answer:
            st.session_state.chat_history.append(
                {"role": "user", "content": user_question.strip()}
            )
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Agent:** {msg['content']}")

    st.markdown("---")
    st.caption(
        "Built for Rooman AI Agent Development Challenge – Knowledge Base Agent (Groq + ChromaDB)"
    )


if __name__ == "__main__":
    main()
