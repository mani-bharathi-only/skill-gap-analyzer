
import pytest

from fastapi.testclient import TestClient

from backend.main import app
from backend import database


@pytest.fixture
def test_database(tmp_path, monkeypatch):

    # Use a temporary database for each test
    temporary_db = tmp_path / "test_skill_gap.db"

    monkeypatch.setattr(
        database,
        "DB_PATH",
        temporary_db
    )

    database.initialize_database()

    return temporary_db


def test_database_initialization(test_database):

    assert test_database.exists()

    jobs = database.get_all_jobs()

    assert len(jobs) == 5


def test_no_duplicate_jobs(test_database):

    # Run initialization a second time
    database.initialize_database()

    jobs = database.get_all_jobs()

    assert len(jobs) == 5


def test_get_all_jobs(test_database):

    jobs = database.get_all_jobs()

    titles = [job["title"] for job in jobs]

    assert "Python Backend Developer" in titles
    assert "Frontend Developer" in titles


def test_get_job_by_id(test_database):

    jobs = database.get_all_jobs()

    first_job = jobs[0]

    result = database.get_job_by_id(
        first_job["id"]
    )

    assert result == first_job


def test_get_nonexistent_job(test_database):

    result = database.get_job_by_id(999999)

    assert result is None


def test_jobs_api(test_database):

    with TestClient(app) as client:

        response = client.get("/jobs")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 5


def test_single_job_api(test_database):

    jobs = database.get_all_jobs()

    job_id = jobs[0]["id"]

    with TestClient(app) as client:

        response = client.get(
            f"/jobs/{job_id}"
        )

        assert response.status_code == 200

        assert response.json()["id"] == job_id


def test_job_not_found_api(test_database):

    with TestClient(app) as client:

        response = client.get(
            "/jobs/999999"
        )

        assert response.status_code == 404

        assert response.json() == {
            "detail": "Job not found"
        }
