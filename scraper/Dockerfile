FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

RUN mkdir -p /logs && chmod 777 /logs

# Sätt gemensam cache-sökväg
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Installera Chromium till den gemensamma sökvägen
RUN python -m playwright install chromium

COPY requirements.txt .
RUN pip install --no-cache-dir flask==3.0.0 flask-cors==4.0.0 psycopg2-binary==2.9.9

COPY scraper.py .

EXPOSE 5001

CMD ["python", "scraper.py"]
