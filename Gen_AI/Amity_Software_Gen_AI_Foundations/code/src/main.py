from data_ingestion import load_pdf, generate_embeddings, store_in_pinecone
from data_retrieval import semantic_search, rerank_results, generate_answer
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings


def run_rag_pipeline(pdf_path, query, pinecone_api_key, google_api_key):
    """Run the full RAG pipeline: ingestion + retrieval + answer generation."""
    
    print("Running Ingestion Pipeline...")
    pages = load_pdf(pdf_path)
    embeddings_list, embedding_model = generate_embeddings(pages)
    index = store_in_pinecone(embeddings_list, pinecone_api_key)
    print(f"Stored {len(embeddings_list)} records in Pinecone.")

    print("\nRunning Retrieval Pipeline...")
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index("amity-database")

    # Recreate embedding model for retrieval
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    search_results = semantic_search(query, embedding_model, index)
    reranked = rerank_results(query, search_results)
    context = "\n\n".join([doc['metadata']['text'] for doc, _ in reranked])

    answer = generate_answer(context, query, google_api_key)

    print("\n--- Final Answer ---")
    print(answer)
    return answer



if __name__ == "__main__":
    pdf_path = "./data/HDFC-Life-Saral-Jeevan-UIN-101N160V05-Policy-Document.pdf"
    pinecone_api_key = "pcsk_5qj9jc_6WPE7Jr4rsB6GKM6nTZXL4EBpgu4oV6j6jh29TTnuEK8ihdZkqwtL9gQnh92T3b"
    google_api_key = "AIzaSyDGcDBJjKJKfWRlkAzM_Gfk54MbC0fW3QM"
    query = "Special surrender value"

    run_rag_pipeline(pdf_path, query, pinecone_api_key, google_api_key)
