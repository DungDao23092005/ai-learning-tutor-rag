import pytest

from src.rag_chain import (
    build_rag_prompt,
    format_retrieved_context,
    generate_rag_answer,
)


class TestFormatRetrievedContext:

    def test_empty_chunks_returns_empty_string(self):
        assert format_retrieved_context([]) == ""

    def test_formats_chunks_with_source_header(self):
        chunks = [
            {"chunk_id": "chunk-1", "page_number": 1, "chunk_index": 1, "text": "Hello", "distance": 0.1},
        ]
        result = format_retrieved_context(chunks)
        assert "[Source 1]" in result
        assert "Page: 1" in result
        assert "Hello" in result

    def test_multiple_chunks_are_separated(self):
        chunks = [
            {"chunk_id": "c1", "page_number": 1, "chunk_index": 1, "text": "A", "distance": 0.1},
            {"chunk_id": "c2", "page_number": 2, "chunk_index": 1, "text": "B", "distance": 0.2},
        ]
        result = format_retrieved_context(chunks)
        assert "---" in result


class TestBuildRagPrompt:

    def test_prompt_contains_question_and_context(self):
        chunks = [
            {"chunk_id": "c1", "page_number": 1, "chunk_index": 1, "text": "Context text.", "distance": 0.1},
        ]
        prompt = build_rag_prompt("What is X?", chunks)
        assert "What is X?" in prompt
        assert "Context text." in prompt

    def test_prompt_contains_rules(self):
        prompt = build_rag_prompt("Test?", [])
        assert "Use only the information from the context" in prompt

    def test_prompt_mentions_source_pages(self):
        prompt = build_rag_prompt("Test?", [])
        assert "source pages" in prompt


class TestGenerateRagAnswer:

    def test_empty_question_raises_error(self):
        with pytest.raises(ValueError, match="Question must not be empty"):
            generate_rag_answer("", [])

    def test_whitespace_question_raises_error(self):
        with pytest.raises(ValueError):
            generate_rag_answer("   ", [])

    def test_no_chunks_returns_fallback_message(self):
        result = generate_rag_answer("What is X?", [])
        assert "cannot find relevant information" in result.lower()
