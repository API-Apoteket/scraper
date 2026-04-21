# Använd Playwrights officiella image som bas
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Installera extra Python-beroenden
COPY requirements.txt .
RUN pip install --no-cache-dir asyncpg redis flask flask-cors prometheus-fastapi-instrumentator

COPY scraper.py .
COPY worker_v3.py .
COPY api_v3.py .

EXPOSE 5001

CMD ["python", "scraper.py"]
