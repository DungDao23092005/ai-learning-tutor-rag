import pytest

from src.quiz_generator import (
    check_quiz_answers,
    extract_json_from_text,
    format_quiz_context,
)


class TestFormatQuizContext:

    def test_empty_chunks_returns_empty_string(self):
        assert format_quiz_context([]) == ""

    def test_chunks_have_source_headers(self):
        chunks = [
            {"chunk_id": "c1", "page_number": 1, "chunk_index": 1, "text": "Content"},
        ]
        result = format_quiz_context(chunks)
        assert "[Source 1]" in result
        assert "Page: 1" in result
        assert "Content" in result


class TestExtractJsonFromText:

    def test_parses_plain_json(self):
        text = '{"questions": [{"question": "Q1", "options": {"A": "Opt1", "B": "Opt2", "C": "Opt3", "D": "Opt4"}, "correct_answer": "A", "explanation": "Exp"}]}'
        result = extract_json_from_text(text)
        assert "questions" in result
        assert len(result["questions"]) == 1

    def test_strips_markdown_code_fences(self):
        text = '```json\n{"questions": []}\n```'
        result = extract_json_from_text(text)
        assert result == {"questions": []}

    def test_strips_plain_code_fences(self):
        text = '```\n{"questions": []}\n```'
        result = extract_json_from_text(text)
        assert result == {"questions": []}


class TestCheckQuizAnswers:

    def test_all_correct_returns_perfect_score(self):
        questions = [
            {
                "question": "Q1?",
                "options": {"A": "A1", "B": "B1", "C": "C1", "D": "D1"},
                "correct_answer": "A",
                "explanation": "E1",
            },
        ]
        user_answers = {0: "A"}
        result = check_quiz_answers(questions, user_answers)
        assert result["score"] == 1
        assert result["total"] == 1
        assert result["results"][0]["is_correct"] is True

    def test_mixed_answers(self):
        questions = [
            {"question": "Q1?", "options": {"A": "", "B": "", "C": "", "D": ""}, "correct_answer": "A", "explanation": "E1"},
            {"question": "Q2?", "options": {"A": "", "B": "", "C": "", "D": ""}, "correct_answer": "B", "explanation": "E2"},
        ]
        user_answers = {0: "A", 1: "C"}
        result = check_quiz_answers(questions, user_answers)
        assert result["score"] == 1
        assert result["total"] == 2
        assert result["results"][0]["is_correct"] is True
        assert result["results"][1]["is_correct"] is False

    def test_result_contains_explanations(self):
        questions = [
            {"question": "Q1?", "options": {"A": "", "B": "", "C": "", "D": ""}, "correct_answer": "A", "explanation": "Because X"},
        ]
        result = check_quiz_answers(questions, {0: "A"})
        assert result["results"][0]["explanation"] == "Because X"
