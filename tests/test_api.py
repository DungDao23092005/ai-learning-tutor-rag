import pytest
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


class TestHealth:

    def test_health_endpoint_returns_ok(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "ai-learning-tutor-rag"


class TestDocuments:

    def test_upload_no_file_returns_422(self):
        response = client.post("/api/documents/upload")
        assert response.status_code == 422

    def test_reset_store_returns_success(self):
        response = client.post("/api/documents/reset")
        assert response.status_code == 200
        assert response.json()["message"] == "Vector store reset successfully."

    def test_get_stats_returns_expected_keys(self):
        response = client.get("/api/documents/stats")
        assert response.status_code == 200
        data = response.json()
        assert "collection_name" in data
        assert "total_items" in data
        assert "persist_path" in data


class TestChat:

    def test_ask_empty_question_returns_400(self):
        response = client.post("/api/chat/ask", json={"question": ""})
        assert response.status_code == 400

    def test_ask_without_document_returns_fallback(self):
        client.post("/api/documents/reset")
        response = client.post("/api/chat/ask", json={"question": "What is AI?"})
        assert response.status_code == 200
        data = response.json()
        assert "cannot find relevant information" in data["answer"].lower()
