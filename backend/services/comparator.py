
from backend.services.parser import SKILLS


def compare_skills(resume_skills, job_skills):

    # Convert lists to sets
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    # 1. Find exact matches
    matched = sorted(resume_set & job_set)

    # 2. Prepare remaining categories
    adjacent = []
    missing = []

    # 3. Check unmatched job requirements
    for skill in sorted(job_set - resume_set):

        # Find related skills in our taxonomy
        related = set(
            SKILLS[skill]["adjacent"]
        )

        # Does the candidate know a related skill?
        transferable = sorted(
            resume_set & related
        )

        if transferable:
            adjacent.append({
                "required_skill": skill,
                "related_skills": transferable
            })

        else:
            missing.append(skill)

    # 4. Return the analysis
    return {
        "matched": matched,
        "adjacent": adjacent,
        "missing": missing
    }
