#!/bin/bash
set -e

echo "🔧 Fixing permissions for UID:GID = ${PUID}:${PGID}"

# Använd $HOME istället för /root
export HOME=/home/user
mkdir -p $HOME/.cache/ms-playwright /logs

# Ladda ner Chromium om det inte finns
if [ ! -d "$HOME/.cache/ms-playwright/chromium-"* ] 2>/dev/null; then
    echo "📦 Downloading Chromium for Playwright..."
    python -m playwright install chromium
    echo "✅ Chromium downloaded!"
fi

exec python scraper.py
