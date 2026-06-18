from typing import Dict, List

import chromadb


CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "ai_tutor_rag_collection"


def get_chroma_client():
    """
    Create a persistent ChromaDB client.

    Data will be saved locally in the chroma_db/ folder.
    """
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_or_create_collection():
    """
    Get or create a ChromaDB collection.
    """
    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "AI Tutor RAG document chunks"
        }
    )

    return collection


def reset_vector_store() -> None:
    """
    Delete and recreate the collection.

    This helps avoid mixing chunks from old uploaded PDFs
    with the current PDF.
    """
    client = get_chroma_client()

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "AI Tutor RAG document chunks"
        }
    )


def store_chunks_in_chroma(embedded_chunks: List[Dict]) -> int:
    """
    Store embedded chunks into ChromaDB.

    Args:
        embedded_chunks: Chunks with embedding vectors.

    Returns:
        Number of chunks stored.
    """
    if not embedded_chunks:
        raise ValueError("No embedded chunks to store.")

    collection = get_or_create_collection()

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in embedded_chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])
        metadatas.append(
            {
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return len(ids)


def search_relevant_chunks(
    query_embedding: List[float],
    top_k: int = 3
) -> List[Dict]:
    """
    Search relevant chunks from ChromaDB using query embedding.

    Args:
        query_embedding: Embedding vector of user's question.
        top_k: Number of relevant chunks to return.

    Returns:
        A list of relevant chunks with text, metadata, and distance.
    """
    collection = get_or_create_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    relevant_chunks = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    for chunk_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances
    ):
        relevant_chunks.append(
            {
                "chunk_id": chunk_id,
                "text": document,
                "page_number": metadata.get("page_number"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distance,
            }
        )

    return relevant_chunks


def get_vector_store_stats() -> Dict:
    """
    Get simple statistics from ChromaDB collection.
    """
    collection = get_or_create_collection()

    return {
        "collection_name": COLLECTION_NAME,
        "total_items": collection.count(),
        "persist_path": CHROMA_DB_PATH,
    }