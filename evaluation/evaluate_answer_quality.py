"""
Answer Quality Evaluation using LLM-as-Judge

Generates sample Q&A pairs from the uploaded document and uses an LLM
to evaluate answer faithfulness, relevance, and completeness.

Usage:
    python -m evaluation.evaluate_answer_quality
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.embedding import create_embedding
from src.rag_chain import generate_rag_answer
from src.vector_store import get_or_create_collection, search_relevant_chunks

from backend.core.provider_factory import get_provider


EVALUATION_QUESTIONS: List[str] = [
    "What is the main topic of this document?",
    "What are the key concepts explained?",
    "Give me a simple example from the content.",
]


JUDGE_PROMPT_TEMPLATE = """
You are an expert evaluator of RAG system outputs.

Evaluate the following answer based on THREE criteria.
Score each criterion from 1 (worst) to 5 (best).

Criteria:
1. Faithfulness: Does the answer stay strictly within the provided context?
2. Relevance: Does the answer directly address the question?
3. Completeness: Does the answer cover all relevant information?

Question: {question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Return ONLY valid JSON:
{{
    "faithfulness": <1-5>,
    "relevance": <1-5>,
    "completeness": <1-5>,
    "overall": <average>,
    "explanation": "<brief explanation>"
}}
"""


def run_answer_evaluation() -> None:
    collection = get_or_create_collection()
    total_items = collection.count()

    print(f"Vector store contains {total_items} chunks.\n")

    if total_items == 0:
        print("No data found. Upload and process a document first.")
        return

    provider = get_provider()
    total_scores = {"faithfulness": [], "relevance": [], "completeness": []}

    for question in EVALUATION_QUESTIONS:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")

        query_embedding = create_embedding(
            text=question,
            task_type="RETRIEVAL_QUERY",
        )

        retrieved_chunks = search_relevant_chunks(
            query_embedding=query_embedding,
            top_k=3,
        )

        if not retrieved_chunks:
            print("No relevant chunks found. Skipping.")
            continue

        answer = generate_rag_answer(
            question=question,
            retrieved_chunks=retrieved_chunks,
        )

        context_text = "\n\n".join(
            f"[Source {i+1}] Page {c['page_number']}: {c['text'][:300]}"
            for i, c in enumerate(retrieved_chunks)
        )

        judge_prompt = JUDGE_PROMPT_TEMPLATE.format(
            question=question,
            context=context_text,
            answer=answer,
        )

        try:
            judge_response = provider.generate_text(
                prompt=judge_prompt,
                model="gemini-2.5-flash-lite",
            )

            cleaned = judge_response.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1]
                if "```" in cleaned:
                    cleaned = cleaned.split("```")[0]
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1]
                if "```" in cleaned:
                    cleaned = cleaned.split("```")[0]

            scores = json.loads(cleaned.strip())

            print(f"  Answer: {answer[:200]}...")
            print(f"  Faithfulness: {scores.get('faithfulness', 'N/A')}/5")
            print(f"  Relevance:    {scores.get('relevance', 'N/A')}/5")
            print(f"  Completeness: {scores.get('completeness', 'N/A')}/5")
            print(f"  Overall:      {scores.get('overall', 'N/A')}/5")
            print(f"  Explanation:  {scores.get('explanation', 'N/A')}")

            for key in total_scores:
                if key in scores:
                    total_scores[key].append(scores[key])

        except Exception as e:
            print(f"  Judge evaluation failed: {e}")
            print(f"  Raw judge response: {judge_response[:300]}")

    print("\n" + "=" * 60)
    print("AGGREGATE RESULTS")
    print("=" * 60)
    for key, values in total_scores.items():
        if values:
            avg = sum(values) / len(values)
            print(f"{key.capitalize():15s}: {avg:.2f}/5 (over {len(values)} questions)")
        else:
            print(f"{key.capitalize():15s}: No data")
    print("=" * 60)


if __name__ == "__main__":
    run_answer_evaluation()
