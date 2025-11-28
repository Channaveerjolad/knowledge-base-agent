 #AI Knowledge Base Agent
   An intelligent Retrieval-Augmented AI Agent that can:
   -Read & understand company documents (PDF/TXT)
   -Build a semantic knowledge base automatically
   -Answer any question with accurate, context-based responses
   -Cite exact sources clearly
   -Powered by Groq Llama 3.1 for ultra-fast inference
   -Stores embeddings using ChromaDB for persistent vector storage

 #Overview
    Modern companies have a lot of documents — policies, resumes, SOPs, HR guidelines, training material, etc.
    Employees waste a lot of time searching through them manually.
    This AI Agent solves that by:
    ✔ Uploading documents once
    ✔ Automatically storing, splitting, embedding, and indexing them
    ✔ Allowing you to ask questions anytime
    ✔ Answering only from the uploaded documents (no hallucination)

 #Features
 ★ Smart Document Processing
   Upload PDF or TXT files
   Auto text extraction (using pypdf)
   Intelligent chunking with overlap for better context retrieval
 ★ Persistent Knowledge Base
   Uses ChromaDB (local storage)
   Stores vector embeddings + metadata
   Works offline and survives restarts
 ★ Local Embeddings (No Cost)
  SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
  Benefits:
   ✔ Free
   ✔ Fast
   ✔ Offline
   ✔ Accurate semantic search
 ★ LLM Response Engine
   Uses Groq Llama 3.1 (8B Instant)
   Ultra-fast inference
   Strictly answers from the retrieved context
   Cites sources automatically
 ★ Streamlit UI
   Sidebar for uploads
   Simple chat-style interaction
   Shows context-aware answers
   
 #Tech Stack
| Layer          | Technology          |
| -------------- | ------------------- |
| UI             | Streamlit           |
| Backend        | Python 3.11         |
| LLM            | Groq Llama 3.1      |
| Vector DB      | ChromaDB            |
| Embeddings     | SentenceTransformer |
| PDF Parsing    | pypdf               |
| Env Management | python-dotenv       |

 #Architecture Diagram
                  ┌────────────────────────────┐
                  │        Streamlit UI        │
                  │────────────────────────────│
                  │ • Document Upload (PDF/TXT)│
                  │ • User Question Input      │
                  │ • Chat-style Responses     │
                  └───────────────┬────────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │      KB Module         │
                     │        (kb.py)         │
                     │────────────────────────│
                     │ • Text Extraction      │
                     │ • Smart Chunking       │
                     │ • Local Embeddings     │
                     │ • Add/Query ChromaDB   │
                     └───────────────┬────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │      ChromaDB (Local)  │
                        │────────────────────────│
                        │ • Stores vector embeddings
                        │ • Metadata (source names)
                        │ • Persistent DB storage
                        └──────────────┬─────────┘
                                       │
                     Top-K Relevant Chunks ▼
                        ┌────────────────────────┐
                        │    Groq Llama 3.1      │
                        │    (8B Instant)        │
                        │────────────────────────│
                        │ • RAG-based answering  │
                        │ • Context-aware output │
                        │ • Strict source usage  │
                        └──────────────┬─────────┘
                                       │
                                       ▼
                       ┌──────────────────────────┐
                       │       Final Answer       │
                       │──────────────────────────│
                       │ • Summaries              │
                       │ • Insights               │
                       │ • Source Citations       │
                       └──────────────────────────┘


