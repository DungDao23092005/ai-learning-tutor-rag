import asyncio

import pytest

from src.embedding import (
    create_embedding,
    create_embeddings_for_chunks_async,
    create_embeddings_for_chunks_parallel,
    get_embedding_stats,
)


class TestGetEmbeddingStats:

    def test_empty_list_returns_zeros(self):
        stats = get_embedding_stats([])
        assert stats["total_embedded_chunks"] == 0
        assert stats["embedding_dimension"] == 0

    def test_returns_correct_dimension(self):
        chunks = [
            {"chunk_id": "c1", "embedding": [0.1, 0.2, 0.3]},
            {"chunk_id": "c2", "embedding": [0.4, 0.5, 0.6]},
        ]
        stats = get_embedding_stats(chunks)
        assert stats["total_embedded_chunks"] == 2
        assert stats["embedding_dimension"] == 3


class TestCreateEmbeddingsParallel:

    def test_empty_list_returns_empty_list(self):
        result = create_embeddings_for_chunks_parallel([])
        assert result == []

    def test_parallel_returns_same_structure(self):
        chunks = [
            {"chunk_id": "c1", "text": "Hello", "page_number": 1, "chunk_index": 1},
        ]
        import pytest
        try:
            result = create_embeddings_for_chunks_parallel(chunks)
            assert len(result) == 1
            assert "embedding" in result[0]
        except ValueError as e:
            if "API key" in str(e) or "missing" in str(e).lower():
                pytest.skip("No API key configured")


class TestCreateEmbeddingsAsync:

    @pytest.mark.asyncio
    async def test_async_returns_empty_for_empty_input(self):
        result = await create_embeddings_for_chunks_async([])
        assert result == []
