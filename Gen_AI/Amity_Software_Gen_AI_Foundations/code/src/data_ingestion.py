from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf(file_path: str):
    """Load PDF and return pages."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(pages)
    return chunks



def generate_embeddings(pages):
    """Generate embeddings for each page."""
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    embeddings_list = []
    print("Generating embedding work is in progress...")
    for page in pages:
        content = page.page_content
        
        embedding = embedding_model.embed_documents([content])[0] 
        embeddings_list.append({"content": content, "embedding": embedding})
        
    return embeddings_list, embedding_model

def store_in_pinecone(embeddings_list, pinecone_api_key, index_name="amity-database"):
    """Store embeddings in Pinecone and return index."""
    pc = Pinecone(api_key=pinecone_api_key)

    # Create index if not exists
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    index = pc.Index(index_name)
    records = [
        {
            "id": f"chunk-{i}",
            "values": item["embedding"],
            "metadata": {"text": item["content"]}
        }
        for i, item in enumerate(embeddings_list)
    ]

    index.upsert(vectors=records, namespace="amity")
    return index

if __name__ == "__main__":
    pdf_path = "./data/HDFC-Life-Saral-Jeevan-UIN-101N160V05-Policy-Document.pdf"
    pinecone_api_key = "pcsk_5qj9jc_6WPE7Jr4rsB6GKM6nTZXL4EBpgu4oV6j6jh29TTnuEK8ihdZkqwtL9gQnh92T3b"

    print("Running Ingestion Pipeline...")
    pages = load_pdf(pdf_path)
    print(f"Loaded {len(pages)} pages.")

    embeddings_list, _ = generate_embeddings(pages)
    index = store_in_pinecone(embeddings_list, pinecone_api_key)

    print(f" Stored {len(embeddings_list)} records in Pinecone.")
