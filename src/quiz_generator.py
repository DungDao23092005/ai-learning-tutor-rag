import json
import re
from typing import Dict, List

from src.rag_chain import generate_text_with_fallback


def format_quiz_context(chunks: List[Dict], max_chunks: int = 12) -> str:
    """
    Format document chunks for quiz generation.
    """
    selected_chunks = chunks[:max_chunks]
    context_parts = []

    for index, chunk in enumerate(selected_chunks, start=1):
        source_header = (
            f"[Source {index}] "
            f"Page: {chunk['page_number']}, "
            f"Chunk ID: {chunk['chunk_id']}"
        )

        context_parts.append(
            f"{source_header}\n{chunk['text']}"
        )

    return "\n\n---\n\n".join(context_parts)


def extract_json_from_text(text: str) -> Dict:
    """
    Extract JSON object from Gemini response.

    Gemini may sometimes wrap JSON in markdown code fences,
    so this function removes those fences before parsing.
    """
    cleaned_text = text.strip()

    cleaned_text = re.sub(
        r"^```json\s*",
        "",
        cleaned_text
    )

    cleaned_text = re.sub(
        r"^```\s*",
        "",
        cleaned_text
    )

    cleaned_text = re.sub(
        r"\s*```$",
        "",
        cleaned_text
    )

    return json.loads(cleaned_text)


def build_quiz_prompt(chunks: List[Dict], number_of_questions: int) -> str:
    """
    Build prompt for quiz generation.
    """
    context = format_quiz_context(chunks)

    prompt = f"""
You are an AI learning tutor.

Create {number_of_questions} multiple-choice questions from the provided document context.

Rules:
1. Use ONLY the provided context.
2. Write all questions in Vietnamese.
3. Each question must have exactly 4 options: A, B, C, D.
4. Only one option is correct.
5. Provide a short explanation for the correct answer.
6. Return ONLY valid JSON.
7. Do not include markdown, code fences, or extra text.

Required JSON format:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": {{
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      }},
      "correct_answer": "A",
      "explanation": "Explanation text"
    }}
  ]
}}

Document context:
{context}
"""
    return prompt.strip()


def generate_quiz(
    chunks: List[Dict],
    number_of_questions: int = 5
) -> List[Dict]:
    """
    Generate quiz questions from document chunks.
    """
    if not chunks:
        raise ValueError("No document chunks available for quiz generation.")

    prompt = build_quiz_prompt(
        chunks=chunks,
        number_of_questions=number_of_questions
    )

    response_text = generate_text_with_fallback(prompt)

    quiz_data = extract_json_from_text(response_text)

    questions = quiz_data.get("questions", [])

    if not questions:
        raise ValueError("No quiz questions were generated.")

    return questions


def check_quiz_answers(
    quiz_questions: List[Dict],
    user_answers: Dict[int, str]
) -> Dict:
    """
    Check user's quiz answers.
    """
    results = []
    score = 0

    for index, question in enumerate(quiz_questions):
        correct_answer = question["correct_answer"]
        selected_answer = user_answers.get(index)

        is_correct = selected_answer == correct_answer

        if is_correct:
            score += 1

        results.append(
            {
                "question": question["question"],
                "selected_answer": selected_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question["explanation"],
            }
        )

    return {
        "score": score,
        "total": len(quiz_questions),
        "results": results,
    }