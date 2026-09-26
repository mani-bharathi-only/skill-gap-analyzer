
import json
from pathlib import Path

import spacy
from spacy.matcher import PhraseMatcher


# 1. Locate our taxonomy file
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "skills.json"
)


# 2. Load the skill taxonomy
with open(DATA_PATH, "r", encoding="utf-8") as file:
    SKILLS = json.load(file)


# 3. Initialize spaCy
nlp = spacy.load("en_core_web_sm")


# 4. Create a case-insensitive phrase matcher
matcher = PhraseMatcher(
    nlp.vocab,
    attr="LOWER"
)


# 5. Register skill names and aliases
for skill_name, details in SKILLS.items():

    names = [skill_name] + details["aliases"]

    patterns = [
        nlp.make_doc(name)
        for name in names
    ]

    matcher.add(skill_name, patterns)


# 6. Extract skills from text
def extract_skills(text: str) -> list[str]:

    doc = nlp(text)

    matches = matcher(doc)

    found_skills = set()

    for match_id, start, end in matches:

        skill_name = nlp.vocab.strings[match_id]

        found_skills.add(skill_name)

    return sorted(found_skills)
