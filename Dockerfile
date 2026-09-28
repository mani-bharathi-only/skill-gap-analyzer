
# Use a lightweight Python image matching the project environment
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Display Python output immediately
ENV PYTHONUNBUFFERED=1

# Copy the dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install the spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy the backend code
COPY backend/ ./backend/

# Create a directory for persistent data
RUN mkdir -p /app/data

# Configure the SQLite database path
ENV DATABASE_PATH=/app/data/skill_gap.db

# Document the port used by FastAPI
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
