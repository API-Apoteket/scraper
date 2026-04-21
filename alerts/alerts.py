#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import datetime
import requests
import os
import time
import json
import logging
import sys
import signal

DB_FILE = os.getenv('DB_FILE', '/data/products.db')
DISCORD_WEBHOOK_FILE = os.getenv('DISCORD_WEBHOOK_FILE', '/run/secrets/discord_webhook')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '1800'))
MIN_DROP_PERCENT = float(os.getenv('MIN_DROP_PERCENT', '5'))
MIN_DROP_AMOUNT = int(os.getenv('MIN_DROP_AMOUNT', '100'))
COOLDOWN_HOURS = int(os.getenv('COOLDOWN_HOURS', '24'))
COOLDOWN_FILE = "/data/alert_cooldown.json"
LOG_DIR = "/logs"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/alerts.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

shutdown_event = False
alerts_sent = 0


def get_webhook():
    try:
        with open(DISCORD_WEBHOOK_FILE, 'r') as f:
            return f.read().strip()
    except:
        return os.getenv('DISCORD_WEBHOOK')


def get_db():
    for attempt in range(3):
        try:
            conn = sqlite3.connect(DB_FILE, timeout=10)
            conn.row_factory = sqlite3.Row
            return conn
        except:
            if attempt < 2:
                time.sleep(2)
    return None


def load_cooldown():
    try:
        with open(COOLDOWN_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}


def save_cooldown(data):
    try:
        with open(COOLDOWN_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass


def send_discord(webhook, title, old_price, new_price, url):
    drop = old_price - new_price
    percent = round((drop / old_price) * 100, 1)
    
    payload = {
        "embeds": [{
            "title": "💸 Prisfall!",
            "description": f"**{title}**",
            "color": 16711680,
            "fields": [
                {"name": "Gammalt", "value": f"{old_price:,} kr".replace(",", " "), "inline": True},
                {"name": "Nytt", "value": f"{new_price:,} kr".replace(",", " "), "inline": True},
                {"name": "Nedgång", "value": f"-{drop:,} kr ({percent}%)".replace(",", " "), "inline": True},
                {"name": "Länk", "value": url}
            ]
        }]
    }
    
    try:
        return requests.post(webhook, json=payload, timeout=10).status_code == 204
    except:
        return False


def check_drops():
    webhook = get_webhook()
    if not webhook:
        logger.error("Ingen webhook konfigurerad")
        return 0
    
    conn = get_db()
    if not conn:
        return 0
    
    try:
        cur = conn.cursor()
        cooldown = load_cooldown()
        now = time.time()
        
        cur.execute("""
            SELECT p.id, p.title, p.url, ph1.price AS old_price, ph2.price AS new_price
            FROM products p
            JOIN price_history ph1 ON p.id = ph1.product_id
            JOIN price_history ph2 ON p.id = ph2.product_id
            WHERE ph1.id < ph2.id
            AND ph2.timestamp = (SELECT MAX(timestamp) FROM price_history WHERE product_id = p.id)
            AND ph1.timestamp = (SELECT MAX(timestamp) FROM price_history 
                                WHERE product_id = p.id AND id < ph2.id)
            AND ph2.price < ph1.price
        """)
        
        alerts_this_run = 0
        
        for row in cur.fetchall():
            drop_amount = row['old_price'] - row['new_price']
            drop_percent = (drop_amount / row['old_price']) * 100
            
            if drop_percent < MIN_DROP_PERCENT and drop_amount < MIN_DROP_AMOUNT:
                continue
            
            last_alert = cooldown.get(str(row['id']), 0)
            if now - last_alert < COOLDOWN_HOURS * 3600:
                continue
            
            if send_discord(webhook, row['title'], row['old_price'], row['new_price'], row['url']):
                cooldown[str(row['id'])] = now
                alerts_this_run += 1
                logger.info(f"Alert: {row['title'][:50]}...")
                time.sleep(1)
        
        save_cooldown(cooldown)
        return alerts_this_run
    finally:
        conn.close()


def signal_handler(signum, frame):
    global shutdown_event
    shutdown_event = True


def main():
    global shutdown_event
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info(f"Alerts startade. Intervall: {CHECK_INTERVAL}s")
    
    while not shutdown_event:
        try:
            sent = check_drops()
            if sent:
                logger.info(f"Skickade {sent} alerts")
        except Exception as e:
            logger.error(f"Fel: {e}")
        
        for _ in range(CHECK_INTERVAL):
            if shutdown_event:
                break
            time.sleep(1)


if __name__ == "__main__":
    main()
