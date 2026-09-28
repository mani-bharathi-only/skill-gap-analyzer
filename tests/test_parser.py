
from backend.services.parser import extract_skills


def test_extract_multiple_skills():
    text = "I know Python, FastAPI and MySQL."

    result = extract_skills(text)

    assert result == [
        "FastAPI",
        "MySQL",
        "Python"
    ]


def test_skill_alias():
    text = "I have experience with Fast API."

    result = extract_skills(text)

    assert result == ["FastAPI"]


def test_duplicate_skills():
    text = "Python, python, PYTHON"

    result = extract_skills(text)

    assert result == ["Python"]


def test_empty_text():
    result = extract_skills("")

    assert result == []


def test_unknown_skill():
    result = extract_skills(
        "Experience with an imaginary technology."
    )

    assert result == []
