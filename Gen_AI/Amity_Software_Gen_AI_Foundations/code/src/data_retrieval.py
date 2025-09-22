from sentence_transformers import CrossEncoder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone


def semantic_search(query, embedding_model, index, top_k=5):
    """Perform semantic search in Pinecone."""
    print(" Searching Pinecone...")
    query_vector = embedding_model.embed_query(query)
    search_results = index.query(
        vector=query_vector, namespace="amity", include_metadata=True, top_k=top_k
    )
    
    return search_results


def rerank_results(query, search_results, top_n=2):
    """Rerank results using CrossEncoder."""
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    print(" Reranking results...")
    pairs = [(query, doc['metadata']['text']) for doc in search_results['matches']]
    scores = reranker.predict(pairs)
    reranked = sorted(
        zip(search_results['matches'], scores), key=lambda x: x[1], reverse=True
    )[:top_n]
   
    return reranked


def generate_answer(context, query, google_api_key):
    """Generate answer using Gemini model."""
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key
    )
    prompt = PromptTemplate.from_template("""
    You are a helpful assistant. Use the provided context to answer the query.
    If the answer is not in the context, say you don't know answer for this query please try with other query or  provide context to me.

    Context:
    {context}

    Query : {query}

    Answer:
    """)
    chain = prompt | model
    result = chain.invoke({"context": context, "query": query})
    return result.content



def get_result(query,pinecone_api_key="pcsk_5qj9jc_6WPE7Jr4rsB6GKM6nTZXL4EBpgu4oV6j6jh29TTnuEK8ihdZkqwtL9gQnh92T3b",google_api_key="AIzaSyDGcDBJjKJKfWRlkAzM_Gfk54MbC0fW3QM"):

    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index("amity-database")
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

    pinecone_api_key = "pcsk_5qj9jc_6WPE7Jr4rsB6GKM6nTZXL4EBpgu4oV6j6jh29TTnuEK8ihdZkqwtL9gQnh92T3b"
    google_api_key = "AIzaSyDGcDBJjKJKfWRlkAzM_Gfk54MbC0fW3QM"



    query = "required document for maturity claims?"
    get_result(query,pinecone_api_key,google_api_key)


