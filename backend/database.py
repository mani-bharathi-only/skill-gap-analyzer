import os
import json
import sqlite3
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent

DB_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "skill_gap.db")
    )
)

SAMPLE_JOBS_PATH = (
    BASE_DIR / "data" / "sample_jobs.json"
)


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection



def initialize_database():
    DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
    )
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL
            )
        """)

        with open(
            SAMPLE_JOBS_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            jobs = json.load(file)

        for job in jobs:
            connection.execute(
                """
                INSERT OR IGNORE INTO jobs
                (title, description)
                VALUES (?, ?)
                """,
                (
                    job["title"],
                    job["description"]
                )
            )


def get_all_jobs():

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT id, title, description
            FROM jobs
            ORDER BY id
            """
        ).fetchall()

        return [dict(row) for row in rows]


def get_job_by_id(job_id: int):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT id, title, description
            FROM jobs
            WHERE id = ?
            """,
            (job_id,)
        ).fetchone()

        return dict(row) if row else None
