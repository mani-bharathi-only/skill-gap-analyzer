
import json
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "learning_resources.json"
)


with open(DATA_PATH, "r", encoding="utf-8") as file:
    RESOURCES = json.load(file)


def generate_roadmap(comparison: dict) -> list:

    roadmap = []

    # 1. Missing skills
    for skill in comparison["missing"]:

        resource = RESOURCES.get(skill, {})

        roadmap.append({
            "skill": skill,
            "category": "missing",
            "priority": 1,
            "description": resource.get(
                "description",
                "Learn the fundamentals of this skill."
            ),
            "resource_url": resource.get("url"),
            "related_skills": []
        })

    # 2. Adjacent skills
    for item in comparison["adjacent"]:

        skill = item["required_skill"]

        resource = RESOURCES.get(skill, {})

        roadmap.append({
            "skill": skill,
            "category": "adjacent",
            "priority": 2,
            "description": resource.get(
                "description",
                "Build on your existing knowledge."
            ),
            "resource_url": resource.get("url"),
            "related_skills": item["related_skills"]
        })

    # 3. Sort by priority
    roadmap.sort(
        key=lambda item: (
            item["priority"],
            item["skill"]
        )
    )

    return roadmap
