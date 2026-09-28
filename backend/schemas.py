
from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):

    resume_text: str = Field(
        min_length=1,
        max_length=50000
    )

    job_text: str = Field(
        min_length=1,
        max_length=50000
    )

    @field_validator("resume_text", "job_text")
    @classmethod
    def validate_text(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Input must not be empty or whitespace only."
            )

        return value
