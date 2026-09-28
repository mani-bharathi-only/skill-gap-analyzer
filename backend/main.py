
from fastapi import FastAPI
from fastapi import HTTPException
from contextlib import asynccontextmanager

from backend.database import initialize_database
from backend.schemas import AnalyzeRequest
from backend.services.parser import extract_skills
from backend.services.comparator import compare_skills
from backend.services.roadmap import generate_roadmap
from backend.database import (
    initialize_database,
    get_all_jobs,
    get_job_by_id
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize database during startup
    initialize_database()

    yield

    # Shutdown cleanup can be added here later


app = FastAPI(
    title="Skill Gap Analyzer",
    description=(
        "An API that identifies skill gaps "
        "between resumes and job descriptions."
    ),
    version="1.0.0",
    lifespan=lifespan
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


@app.get("/jobs")
def list_jobs():
    return get_all_jobs()


@app.get("/jobs/{job_id}")
def get_job(job_id: int):

    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job
