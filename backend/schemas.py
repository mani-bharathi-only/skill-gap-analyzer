
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):

    resume_text: str = Field(
        min_length=1,
        max_length=50000
    )

    job_text: str = Field(
        min_length=1,
        max_length=50000
    )
