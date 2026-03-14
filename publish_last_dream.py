#!/usr/bin/env python3
import sqlite3
import os
import requests
import sys

DB_PATH = "/tmp/ulibka.db"
BOT_TOKEN = os.environ.get('DREAMS_BOT_TOKEN', '8615351463:AAH8Xob7ORW74re-oge1kw6q6ryXrMDvNuI')
CHANNEL_ID = "-1003370068766"  # @ulybka_plus_dreams

def get_last_dream():
    """Получает последний сон из БД"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, bot_name, dream_text, image_url, created_at 
        FROM dreams 
        ORDER BY id DESC LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    return row

def publish_dream(dream):
    """Публикует сон в Telegram"""
    if not dream:
        print("❌ Нет снов для публикации")
        return False
    
    dream_id, bot_name, dream_text, image_url, created_at = dream
    
    # Формируем сообщение
    message = f"🌙 *Сон бота {bot_name}*\n\n"
    message += f"{dream_text}\n\n"
    message += f"🕐 {created_at}"
    
    if image_url:
        # Отправляем с картинкой
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            'chat_id': CHANNEL_ID,
            'photo': image_url,
            'caption': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, data=data)
    else:
        # Отправляем только текст
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': CHANNEL_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print(f"✅ Сон #{dream_id} опубликован в канале")
        return True
    else:
        print(f"❌ Ошибка: {response.text}")
        return False

if __name__ == "__main__":
    dream = get_last_dream()
    publish_dream(dream)
