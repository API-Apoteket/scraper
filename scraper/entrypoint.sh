#!/bin/bash
set -e

export PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Ladda ner Chromium om det saknas (första start med tom volym)
if [ ! -d "/ms-playwright/chromium-"* ] 2>/dev/null; then
    echo "📦 Downloading Chromium to persistent volume..."
    python -m playwright install chromium
    echo "✅ Chromium cached!"
fi

exec python scraper.py
