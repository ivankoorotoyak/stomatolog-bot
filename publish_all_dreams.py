#!/usr/bin/env python3
import sqlite3
import os
import requests
import time

DB_PATH = "/tmp/ulibka.db"
BOT_TOKEN = os.environ.get('DREAMS_BOT_TOKEN', '8615351463:AAH8Xob7ORW74re-oge1kw6q6ryXrMDvNuI')
CHANNEL_ID = "-1003370068766"  # @ulybka_plus_dreams
PUBLISHED_LOG = "/tmp/published_dreams.log"

def get_published_ids():
    """Получает ID уже опубликованных снов"""
    try:
        with open(PUBLISHED_LOG, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def mark_as_published(dream_id):
    """Отмечает сон как опубликованный"""
    with open(PUBLISHED_LOG, 'a') as f:
        f.write(f"{dream_id}\n")

def get_unpublished_dreams():
    """Получает неопубликованные сны"""
    published = get_published_ids()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, bot_name, dream_text, image_url, created_at 
        FROM dreams 
        ORDER BY id ASC
    """)
    all_dreams = cursor.fetchall()
    conn.close()
    
    unpublished = [d for d in all_dreams if str(d[0]) not in published]
    return unpublished

def publish_dream(dream):
    """Публикует сон в Telegram"""
    dream_id, bot_name, dream_text, image_url, created_at = dream
    
    # Формируем сообщение
    message = f"🌙 *Сон бота {bot_name}*\n\n"
    message += f"{dream_text}\n\n"
    message += f"🕐 {created_at}"
    
    if image_url and image_url.startswith('http'):
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
        print(f"✅ Сон #{dream_id} опубликован")
        mark_as_published(dream_id)
        return True
    else:
        print(f"❌ Ошибка при публикации #{dream_id}: {response.text}")
        return False

def main():
    print("🔍 Поиск неопубликованных снов...")
    dreams = get_unpublished_dreams()
    
    if not dreams:
        print("✅ Все сны уже опубликованы")
        return
    
    print(f"📤 Найдено {len(dreams)} снов для публикации")
    
    for dream in dreams:
        publish_dream(dream)
        time.sleep(1)  # Пауза между сообщениями

if __name__ == "__main__":
    main()
