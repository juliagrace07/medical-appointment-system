import os
import uuid

import chromadb


CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "/app/chroma_data",
)

COLLECTION_NAME = "medical_ai_cache"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def search_cached_answer(
    user_question: str,
    threshold: float = 0.30,
):
    """
    Search the semantic cache for a previously answered question.

    ChromaDB returns a distance score where lower values indicate
    greater similarity. A cached answer is reused when the distance
    is below the configured threshold.
    """

    if not user_question.strip():
        return None

    results = collection.query(
        query_texts=[user_question],
        n_results=1,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    if not results.get("ids") or not results["ids"][0]:
        return None

    distance = results["distances"][0][0]
    metadata = results["metadatas"][0][0]

    if distance <= threshold:
        return {
            "answer": metadata.get("answer", ""),
            "matched_question": results["documents"][0][0],
            "distance": distance,
        }

    return None


def save_answer_to_cache(
    user_question: str,
    ai_answer: str,
):
    """
    Store an AI response in the ChromaDB semantic cache.
    """

    if not user_question.strip() or not ai_answer.strip():
        return None

    item_id = str(uuid.uuid4())

    collection.add(
        ids=[item_id],
        documents=[user_question],
        metadatas=[
            {
                "answer": ai_answer,
            }
        ],
    )

    return item_id
