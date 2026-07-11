import pytest

from src.vector_store import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    get_or_create_collection,
    get_vector_store_stats,
)


class TestGetOrCreateCollection:

    def test_returns_collection_with_correct_name(self):
        collection = get_or_create_collection()
        assert collection.name == COLLECTION_NAME

    def test_returns_persistent_collection(self):
        collection = get_or_create_collection()
        assert collection.count() >= 0


class TestGetVectorStoreStats:

    def test_returns_expected_keys(self):
        stats = get_vector_store_stats()
        assert "collection_name" in stats
        assert "total_items" in stats
        assert "persist_path" in stats

    def test_collection_name_matches_constant(self):
        stats = get_vector_store_stats()
        assert stats["collection_name"] == COLLECTION_NAME

    def test_persist_path_matches_constant(self):
        stats = get_vector_store_stats()
        assert stats["persist_path"] == CHROMA_DB_PATH
