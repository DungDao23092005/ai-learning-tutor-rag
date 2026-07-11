"""
Retrieval Evaluation Script

Measures retrieval precision and recall using synthetic test queries.
Each test case has a known relevant chunk_id to check if the retriever
finds the correct source.

Usage:
    python -m evaluation.evaluate_retrieval
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.embedding import create_embedding
from src.vector_store import get_or_create_collection, search_relevant_chunks


TEST_QUERIES: List[Dict] = [
    {
        "question": "What is the main topic of this document?",
        "expected_page": 1,
    },
]


def compute_retrieval_metrics(
    results: List[Dict],
) -> Dict:
    total = len(results)
    if total == 0:
        return {"precision_at_1": 0, "precision_at_3": 0, "recall_at_k": 0}

    hits_at_1 = sum(
        1 for r in results if r.get("hit_at_1")
    )
    hits_at_3 = sum(
        1 for r in results if r.get("hit_at_3")
    )

    return {
        "total_queries": total,
        "precision_at_1": round(hits_at_1 / total, 4),
        "precision_at_3": round(hits_at_3 / total, 4),
        "hits_at_1": hits_at_1,
        "hits_at_3": hits_at_3,
    }


def run_retrieval_evaluation() -> None:
    collection = get_or_create_collection()
    total_items = collection.count()

    print(f"Vector store contains {total_items} chunks.\n")

    if total_items == 0:
        print("No data found. Upload and process a document first.")
        return

    if not TEST_QUERIES:
        print("No test queries defined. Add sample queries to evaluate_retrieval.py")
        print("Example: {'question': '...', 'expected_page': 1}")
        return

    results = []

    for query in TEST_QUERIES:
        question = query["question"]
        expected_page = query.get("expected_page")

        query_embedding = create_embedding(
            text=question,
            task_type="RETRIEVAL_QUERY",
        )

        retrieved = search_relevant_chunks(
            query_embedding=query_embedding,
            top_k=3,
        )

        hit_at_1 = False
        hit_at_3 = False

        if retrieved:
            if expected_page and retrieved[0].get("page_number") == expected_page:
                hit_at_1 = True

            for chunk in retrieved:
                if expected_page and chunk.get("page_number") == expected_page:
                    hit_at_3 = True

        results.append({
            "question": question,
            "expected_page": expected_page,
            "retrieved_pages": [c.get("page_number") for c in retrieved],
            "hit_at_1": hit_at_1,
            "hit_at_3": hit_at_3,
        })

        status = "✓" if hit_at_1 else "✗"
        print(
            f"{status} Q: {question[:60]:60s} "
            f"Expected page: {expected_page} "
            f"Got pages: {[c.get('page_number') for c in retrieved]}"
        )

    metrics = compute_retrieval_metrics(results)

    print("\n" + "=" * 60)
    print("RETRIEVAL EVALUATION RESULTS")
    print("=" * 60)
    print(f"Total queries:         {metrics['total_queries']}")
    print(f"Precision@1:           {metrics['precision_at_1']:.2%}")
    print(f"Precision@3:           {metrics['precision_at_3']:.2%}")
    print(f"Hits@1:                {metrics['hits_at_1']}/{metrics['total_queries']}")
    print(f"Hits@3:                {metrics['hits_at_3']}/{metrics['total_queries']}")
    print("=" * 60)


if __name__ == "__main__":
    run_retrieval_evaluation()
