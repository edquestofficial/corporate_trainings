# Retrieval-Augmented Generation (RAG) with Pinecone, LangChain & Gemini

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline using **Pinecone**, **LangChain**, **HuggingFace embeddings**, and **Google Gemini**.  

The system is designed in two parts:  
1. **Ingestion pipeline** → processes PDF documents, generates embeddings, and stores them in Pinecone.  
2. **Retrieval pipeline** → queries Pinecone, reranks results, and generates final answers using Gemini.  

A main orchestrator script ties both pipelines together for a complete workflow.

---

## Environment Setup

This project uses [`uv`](https://github.com/astral-sh/uv), a modern Python package manager, to simplify dependency management and virtual environment setup.  

### 1. Install uv
```bash
pip install uv


###
# 2. Create a new project
    uv init rag-pipeline
    cd rag-pipeline


# 3. (Optional) Create a virtual environment manually

    If you prefer using venv:
##
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

##

4. #Install dependencies with uv

    You can add dependencies one by one with uv add <package>, or install them all at once:

uv add \
    "langchain>=0.3.27" \
    "langchain-community>=0.3.29" \
    "langchain-core>=0.3.75" \
    "langchain-google-genai>=2.1.12" \
    "langchain-huggingface>=0.3.1" \
    "langchain-text-splitters>=0.3.11" \
    "langgraph>=0.6.7" \
    "pinecone>=7.3.0" \
    "pinecone-client==5.0.1" \
    "pypdf>=6.0.0" \
    "sentence-transformers==3.0.1" \
    "torch>=2.8.0" \
    "transformers>=4.56.1"

# 5. Verify installation
    uv pip list
###
📂 Project Structure
project/
│── ingestion_pipeline.py     # PDF → Embeddings → Pinecone
│── retrieval_pipeline.py     # Query → Search → Rerank → Answer
│── main.py                   # Orchestrates ingestion + retrieval
│── data/science_10th_class.pdf    # Example input PDF
│── README.md                 # Documentation

###
🔑 API Keys Setup

You will need:

Pinecone API Key → Get from Pinecone 

Google API Key → Get from Google AI 

Update the keys in your code:

pinecone_api_key = "YOUR_PINECONE_API_KEY"
google_api_key = "YOUR_GOOGLE_API_KEY"

Running the Project
Run ingestion pipeline
python ingestion_pipeline.py

Run retrieval pipeline
python retrieval_pipeline.py

Run the full pipeline
python main.py