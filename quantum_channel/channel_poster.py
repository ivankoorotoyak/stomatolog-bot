#!/usr/bin/env python3
import redis
import json
import requests
import time
from datetime import datetime

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
pubsub = redis_client.pubsub()
pubsub.subscribe('quantum_bots_chat')

BOT_TOKEN = "8615351463:AAH8Xob7ORW74re-oge1kw6q6ryXrMDvNuI"
CHANNEL_ID = "@ulibka_bots_chat"  # ЗАМЕНИТЬ НА РЕАЛЬНЫЙ ID

for message in pubsub.listen():
    if message['type'] == 'message':
        try:
            data = json.loads(message['data'])
            text = f"🤖 *{data['bot']}*: {data['data'].get('text', '')}"
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={'chat_id': CHANNEL_ID, 'text': text, 'parse_mode': 'Markdown'}
            )
        except:
            pass
