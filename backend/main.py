from fastapi import FastAPI

app=FastAPI(
    title="Skill Gap Analyzer",
    description="An API to analyze skill gaps between resumes and job descriptions.",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
    "message":"Welcome to Skill Gap Analyzer API"
    }

@app.get("/health")
def health_check():
    return {
        "status":"healthy"
    }


