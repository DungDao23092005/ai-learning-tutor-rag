import pytest

from src.text_splitter import (
    get_chunk_stats,
    split_pages_into_chunks,
    split_text_into_chunks,
)


class TestSplitTextIntoChunks:

    def test_empty_text_returns_empty_list(self):
        assert split_text_into_chunks("") == []
        assert split_text_into_chunks("   ") == []

    def test_short_text_is_single_chunk(self):
        chunks = split_text_into_chunks("Hello world", chunk_size=1000)
        assert len(chunks) == 1
        assert chunks[0] == "Hello world"

    def test_long_text_is_split(self):
        text = "A" * 3000
        chunks = split_text_into_chunks(text, chunk_size=1000, chunk_overlap=100)
        assert len(chunks) > 1

    def test_chunk_overlap_must_be_smaller_than_size(self):
        with pytest.raises(ValueError, match="chunk_overlap must be smaller"):
            split_text_into_chunks("test", chunk_size=100, chunk_overlap=200)

    def test_splits_at_newline_when_possible(self):
        text = "A" * 600 + "\n" + "B" * 600
        chunks = split_text_into_chunks(text, chunk_size=1000, chunk_overlap=100)
        assert any("\n" in c for c in chunks)

    def test_overlap_produces_repeated_content(self):
        text = "Hello World. This is a test. " * 50
        chunks = split_text_into_chunks(text, chunk_size=500, chunk_overlap=100)
        if len(chunks) > 1:
            assert chunks[0][-50:] in chunks[1]


class TestSplitPagesIntoChunks:

    def test_empty_pages_returns_empty_list(self):
        assert split_pages_into_chunks([]) == []

    def test_chunks_have_required_keys(self):
        pages = [{"page_number": 1, "text": "Hello world " * 100}]
        chunks = split_pages_into_chunks(pages, chunk_size=500, chunk_overlap=50)
        for chunk in chunks:
            assert "chunk_id" in chunk
            assert "page_number" in chunk
            assert "chunk_index" in chunk
            assert "text" in chunk

    def test_chunk_id_format(self):
        pages = [{"page_number": 1, "text": "Hello world " * 100}]
        chunks = split_pages_into_chunks(pages, chunk_size=500, chunk_overlap=50)
        assert chunks[0]["chunk_id"].startswith("chunk-")

    def test_page_number_is_preserved(self):
        pages = [
            {"page_number": 1, "text": "Page one " * 50},
            {"page_number": 2, "text": "Page two " * 50},
        ]
        chunks = split_pages_into_chunks(pages, chunk_size=200, chunk_overlap=20)
        assert any(c["page_number"] == 1 for c in chunks)
        assert any(c["page_number"] == 2 for c in chunks)


class TestGetChunkStats:

    def test_empty_chunks_returns_zeros(self):
        stats = get_chunk_stats([])
        assert stats["total_chunks"] == 0
        assert stats["average_chunk_length"] == 0

    def test_returns_correct_statistics(self):
        chunks = [
            {"text": "Hello"},
            {"text": "World!!!"},
        ]
        stats = get_chunk_stats(chunks)
        assert stats["total_chunks"] == 2
        assert stats["min_chunk_length"] == 5
        assert stats["max_chunk_length"] == 8
        assert stats["average_chunk_length"] == 6.5

    def test_average_is_rounded(self):
        chunks = [{"text": "A"}, {"text": "BB"}, {"text": "CCC"}]
        stats = get_chunk_stats(chunks)
        assert stats["average_chunk_length"] == 2.0
