FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

RUN mkdir -p /logs && chmod 777 /logs

# Symlink för cache
RUN ln -sf /ms-playwright /root/.cache/ms-playwright 2>/dev/null || true

# VIKTIGT: Installera Python-paket FRÅN requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py .

EXPOSE 5001

CMD ["python", "scraper.py"]
