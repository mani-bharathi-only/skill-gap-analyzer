
from backend.services.comparator import compare_skills


def test_exact_matches():

    result = compare_skills(
        ["Python", "MySQL"],
        ["Python", "MySQL"]
    )

    assert result["matched"] == [
        "MySQL",
        "Python"
    ]

    assert result["missing"] == []
    assert result["adjacent"] == []


def test_missing_skills():

    result = compare_skills(
        ["Python"],
        ["Python", "Docker"]
    )

    assert result["matched"] == ["Python"]
    assert result["missing"] == ["Docker"]


def test_adjacent_skills():

    result = compare_skills(
        ["Flask"],
        ["FastAPI"]
    )

    assert result["adjacent"] == [
        {
            "required_skill": "FastAPI",
            "related_skills": ["Flask"]
        }
    ]


def test_duplicate_requirements():

    result = compare_skills(
        ["Python"],
        ["Python", "Python", "Docker"]
    )

    assert result["matched"] == ["Python"]
    assert result["missing"] == ["Docker"]


def test_no_job_requirements():

    result = compare_skills(
        ["Python"],
        []
    )

    assert result == {
        "matched": [],
        "adjacent": [],
        "missing": []
    }
