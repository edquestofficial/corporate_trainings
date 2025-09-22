# Retrieval-Augmented Generation (RAG) with Pinecone, LangChain & Gemini

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline using **Pinecone**, **LangChain**, **HuggingFace embeddings**, and **Google Gemini**.  

The system is designed in two parts:  
1. **Ingestion pipeline** → processes PDF documents, generates embeddings, and stores them in Pinecone.  
2. **Retrieval pipeline** → queries Pinecone, reranks results, and generates final answers using Gemini.  

A main orchestrator script ties both pipelines together for a complete workflow.

---
##### python setup 

### Install Python

 Before setting up the project, you need Python 3.10+ installed.

# Windows

Download Python from python.org/downloads

During installation, go with customize installationand  check ✅ “Add Python to PATH”.

## Verify installation:

python --version


## Environment Setup

Initial Setup to setup the project

Step 1:
Open powershell:
run: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

if you are using mac and linux you can follow this link 

https://docs.astral.sh/uv/getting-started/installation/ 

Step 2:
Check if UV installed
Run: uv --version
Run: uv --help

Step 3:
Go to your project directory
Run: uv init

Step 4:
To icreate virtual environment 
uv venv

Activate your virtual environment

source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows


step 5:
#Install dependencies with uv

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

