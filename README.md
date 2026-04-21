# 🕷️ Web Scraper Platform

[![Build and Push Images](https://github.com/blixten85/scraper/actions/workflows/docker-build.yml/badge.svg)](https://github.com/blixten85/scraper/actions/workflows/docker-build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Lättviktig, konfigurerbar web scraping-plattform med WebUI, API och prisbevakning.**

## ✨ Funktioner

| Funktion | Beskrivning |
|----------|-------------|
| 🔍 **Multi-site scraping** | Skrapa valfri e-handelssida med CSS-selektorer |
| 🎨 **WebUI** | Konfigurera och övervaka via webbgränssnitt (port 3000) |
| 📡 **REST API** | Hämta data programmatiskt (port 8000) |
| 🔔 **Prisbevakning** | Discord-notiser vid prisfall |
| 💾 **SQLite** | Enkel, filbaserad databas - ingen extra infrastruktur |
| 🐳 **Docker** | Kör allt med en docker compose up |
| 🏷️ **Generisk** | Fungerar med Inet.se, Komplett, Webhallen, m.fl. |

## 🚀 Snabbstart

```bash
# 1. Klona repot
git clone https://github.com/blixten85/scraper.git
cd scraper

# 2. Skapa secrets-mapp och Discord webhook
mkdir -p secrets
echo "din-discord-webhook-url" > secrets/discord_webhook.txt

# 3. Skapa data-mappar
mkdir -p data logs

# 4. Starta
docker compose up -d

# 5. Öppna WebUI
# http://localhost:3000
