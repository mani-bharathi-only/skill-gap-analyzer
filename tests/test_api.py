
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_analyze():

    response = client.post(
        "/analyze",
        json={
            "resume_text": "Python, Flask, MySQL",
            "job_text": "Python, FastAPI, Docker"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["matched"] == ["Python"]

    assert data["missing"] == ["Docker"]

    assert data["adjacent"] == [
        {
            "required_skill": "FastAPI",
            "related_skills": ["Flask"]
        }
    ]

    assert len(data["roadmap"]) == 2


def test_empty_resume():

    response = client.post(
        "/analyze",
        json={
            "resume_text": "",
            "job_text": "Python developer"
        }
    )

    assert response.status_code == 422


def test_whitespace_only_resume():

    response = client.post(
        "/analyze",
        json={
            "resume_text": "     ",
            "job_text": "Python developer"
        }
    )

    assert response.status_code == 422
