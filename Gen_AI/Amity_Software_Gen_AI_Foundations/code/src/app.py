from fastapi import FastAPI, Query
from data_retrieval import get_result

# FastAPI metadata for docs
app = FastAPI(
    title="Amity RAG API",
    description="""
An API built with FastAPI to perform **Retrieval-Augmented Generation (RAG)** 
using Pinecone for vector search and Gemini for answer generation.

### Features:
- Ask natural language queries over indexed documents
- Get responses generated using RAG pipeline
    """,
    version="1.0.0",
    
)


@app.get("/query", summary="Ask a Question", tags=["RAG Pipeline"])
async def ask(
    query: str = Query(
        ...,
        description="Your natural language query. Example: 'What is the special surrender value?'"
    )
):
    """
    Perform **semantic search + reranking + Gemini answer generation**.

    - Takes a query string as input
    - Searches Pinecone vector DB for relevant context
    - Reranks results using CrossEncoder
    - Generates a final answer using Gemini
    """
    result = get_result(query)
    return {"query": query, "answer": result}


# from fastapi import FastAPI
# from pydantic import BaseModel
# from data_retrieval import get_result

# # Initialize FastAPI app
# app = FastAPI()

# # Define request body
# class QueryRequest(BaseModel):
#     query: str

# # Define route
# @app.get("/ask")
# async def ask(query: str):
#     result = get_result(query) 
#     return {"query": query, "answer": result}



