
from fastapi import FastAPI

from backend.schemas import AnalyzeRequest
from backend.services.parser import extract_skills
from backend.services.comparator import compare_skills
from backend.services.roadmap import generate_roadmap


app = FastAPI(
    title="Skill Gap Analyzer",
    description=(
        "An API that identifies skill gaps "
        "between resumes and job descriptions."
    ),
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Skill Gap Analyzer API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }



@app.post("/analyze")
def analyze_skills(request: AnalyzeRequest):

    # Extract skills
    resume_skills = extract_skills(
        request.resume_text
    )

    job_skills = extract_skills(
        request.job_text
    )

    # Compare skills
    comparison = compare_skills(
        resume_skills,
        job_skills
    )

    # Generate learning roadmap
    roadmap = generate_roadmap(
        comparison
    )

    # Return the complete analysis
    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched": comparison["matched"],
        "adjacent": comparison["adjacent"],
        "missing": comparison["missing"],
        "roadmap": roadmap
    }
