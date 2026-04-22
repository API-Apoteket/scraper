#!/bin/bash
set -e

echo "🔧 Fixing permissions for UID:GID = ${PUID}:${PGID}"

# Skapa /logs med rätt rättigheter
mkdir -p /logs
chown -R ${PUID}:${PGID} /logs 2>/dev/null || true

exec python alerts.py
