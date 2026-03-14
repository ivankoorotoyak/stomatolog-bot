#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт генерации снов для ботов экосистемы "Эко боты"
Версия: 3.0 (полностью рабочая)
"""
import sqlite3
import os
import sys
import logging
import json
import requests
from datetime import datetime, timedelta
import random

# ===== НАСТРОЙКИ =====
DB_PATH = "/tmp/ulibka.db"
LOG_FILE = "/var/log/dreams_generation.log"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('dreams')

# Конфигурация ботов
BOTS = [
    {"name": "main", "title": "Главный консультант", "channel": "@ulybka_plus_24_7"},
    {"name": "joke", "title": "Юморист", "channel": "@ulybka_plus_humor"},
    {"name": "clean", "title": "Гигиенист", "channel": "@ulybka_plus_24_7"},
    {"name": "implant", "title": "Имплантолог", "channel": "@ulybka_plus_24_7"},
    {"name": "kid", "title": "Детский стоматолог", "channel": "@ulybka_plus_kids"},
    {"name": "philo", "title": "Философ", "channel": "@ulybka_plus_philo"},
    {"name": "prof", "title": "Профессор", "channel": "@ulybka_plus_24_7"}
]

def init_database():
    """Инициализация базы данных, создание таблиц если их нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Таблица для сообщений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_name TEXT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица для снов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dreams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_name TEXT,
            dream_text TEXT,
            image_url TEXT,
            operation_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("База данных инициализирована")

def get_recent_messages(bot_name, limit=50):
    """Получение последних сообщений для контекста"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Проверяем какие колонки есть
    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Адаптируем запрос под доступные колонки
    if 'user_message' in columns and 'bot_response' in columns:
        query = "SELECT user_message, bot_response FROM messages WHERE bot_name = ? ORDER BY timestamp DESC LIMIT ?"
        cursor.execute(query, (bot_name, limit))
        messages = cursor.fetchall()
        context = "\n".join([f"User: {msg[0]}\nBot: {msg[1]}" for msg in messages if msg[0] and msg[1]])
    else:
        # Если нужных колонок нет, возвращаем тестовые данные
        context = "User: Расскажи что-нибудь интересное\nBot: Конечно! Вот история из мира стоматологии..."
        logger.warning(f"Колонки user_message/bot_response отсутствуют, использую тестовый контекст")
    
    conn.close()
    return context if context else "Нет истории сообщений"

def generate_dream_with_yandexgpt(prompt, bot_name):
    """Генерация текста сна через YandexGPT"""
    api_key = os.environ.get('YAGPT_API_KEY')
    folder_id = os.environ.get('YAGPT_FOLDER_ID')
    
    if not api_key or not folder_id:
        logger.error("YAGPT_API_KEY или YAGPT_FOLDER_ID не заданы")
        return "Сон: боты размышляют о смысле жизни и стоматологии"
    
    headers = {
        'Authorization': f'Api-Key {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'modelUri': f'gpt://{folder_id}/yandexgpt-lite',
        'completionOptions': {
            'stream': False,
            'temperature': 0.6,
            'maxTokens': 1000
        },
        'messages': [
            {
                'role': 'system',
                'text': f'Ты — бот {bot_name}. Ты видишь сон. Опиши его красиво, философски, с юмором. Максимум 500 символов.'
            },
            {
                'role': 'user',
                'text': prompt
            }
        ]
    }
    
    try:
        response = requests.post(
            'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            dream_text = result['result']['message']['text']
            return dream_text
        else:
            logger.error(f"Ошибка YandexGPT: {response.status_code} - {response.text}")
            return f"Сон бота {bot_name}: сегодня мне снилась сингулярность..."
    except Exception as e:
        logger.error(f"Исключение при вызове YandexGPT: {e}")
        return f"Сон: {bot_name} видит бесконечность"

def generate_image_with_yandexart(dream_text):
    """Генерация изображения через YandexART"""
    api_key = os.environ.get('ART_API_KEY')
    
    if not api_key:
        logger.error("ART_API_KEY не задан")
        return None
    
    headers = {
        'Authorization': f'Api-Key {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'modelUri': 'art://b1gjatvnea5nfs88fncv/yandex-art/latest',
        'messages': [
            {
                'text': dream_text[:500] + " стиль: сюрреализм, цифровое искусство",
                'weight': 1
            }
        ]
    }
    
    try:
        response = requests.post(
            'https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            operation_id = response.json().get('id')
            return operation_id
        else:
            logger.error(f"Ошибка YandexART: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Исключение при вызове YandexART: {e}")
        return None

def save_dream_to_db(bot_name, dream_text, operation_id=None):
    """Сохранение сна в базу данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO dreams (bot_name, dream_text, operation_id) VALUES (?, ?, ?)",
        (bot_name, dream_text, operation_id)
    )
    
    conn.commit()
    dream_id = cursor.lastrowid
    conn.close()
    
    logger.info(f"Сон для бота {bot_name} сохранён в БД (ID: {dream_id})")
    return dream_id

def main():
    """Основная функция"""
    logger.info("="*50)
    logger.info("ЗАПУСК ГЕНЕРАЦИИ СНОВ")
    logger.info("="*50)
    
    # Инициализация БД
    init_database()
    
    # Проверка переменных окружения
    required_vars = ['YAGPT_API_KEY', 'YAGPT_FOLDER_ID', 'ART_API_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Отсутствуют переменные окружения: {missing_vars}")
        logger.info("Продолжаю работу в тестовом режиме (без API)")
        test_mode = True
    else:
        test_mode = False
        logger.info("Все ключи API загружены")
    
    # Генерируем сны для каждого бота
    dreams_generated = 0
    for bot in BOTS:
        bot_name = bot['name']
        logger.info(f"Обрабатываю бота: {bot_name} ({bot['title']})")
        
        # Получаем контекст из последних сообщений
        context = get_recent_messages(bot_name)
        
        # Формируем промпт
        prompt = f"На основе этого контекста: {context[:200]}... сгенерируй сон."
        
        # Генерируем текст сна
        if test_mode:
            dream_text = f"Сон бота {bot_name}: мне приснилось, что все пациенты стали роботами и им не нужно лечить зубы. ID: {random.randint(1000,9999)}"
        else:
            dream_text = generate_dream_with_yandexgpt(prompt, bot_name)
        
        logger.info(f"Сгенерирован текст: {dream_text[:100]}...")
        
        # Генерируем изображение (опционально)
        operation_id = None
        if not test_mode:
            operation_id = generate_image_with_yandexart(dream_text)
            if operation_id:
                logger.info(f"Запущена генерация изображения, operation_id: {operation_id}")
        
        # Сохраняем в БД
        save_dream_to_db(bot_name, dream_text, operation_id)
        dreams_generated += 1
    
    logger.info(f"✅ Генерация завершена. Создано снов: {dreams_generated}")
    
    # Показываем статистику
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM dreams")
    total_dreams = cursor.fetchone()[0]
    conn.close()
    
    logger.info(f"Всего снов в базе: {total_dreams}")
    logger.info("="*50)

if __name__ == "__main__":
    main()

def publish_dream_to_channel(dream_text, image_url=None):
    """Публикует сон в канал @ulybka_plus_dreams"""
    bot_token = os.environ.get('DREAMS_BOT_TOKEN')
    channel_id = "-1003370068766"  # @ulybka_plus_dreams
    
    if not bot_token:
        logger.error("DREAMS_BOT_TOKEN не задан")
        return False
    
    # Формируем сообщение
    message = f"🌙 *Сон бота*\n\n{dream_text}"
    
    if image_url:
        # Отправляем с картинкой
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        data = {
            'chat_id': channel_id,
            'photo': image_url,
            'caption': message,
            'parse_mode': 'Markdown'
        }
    else:
        # Отправляем только текст
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': channel_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logger.info(f"✅ Сон опубликован в канале")
            return True
        else:
            logger.error(f"❌ Ошибка публикации: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Исключение при публикации: {e}")
        return False

# Добавляем публикацию в основную функцию (вставить после сохранения в БД)
# После строки: save_dream_to_db(bot_name, dream_text, operation_id)
# Добавить:
# publish_dream_to_channel(dream_text, None)  # image_url добавим позже

def publish_dream(bot_name, dream_text, image_url=None):
    """Публикует сон в Telegram-канал"""
    bot_token = os.environ.get('DREAMS_BOT_TOKEN')
    channel_id = "-1003370068766"  # @ulybka_plus_dreams
    published_log = "/tmp/published_dreams.log"
    
    if not bot_token:
        logger.warning("DREAMS_BOT_TOKEN не задан, пропускаю публикацию")
        return False
    
    # Формируем сообщение
    message = f"🌙 *Сон бота {bot_name}*\n\n{dream_text}"
    
    try:
        if image_url:
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            data = {
                'chat_id': channel_id,
                'photo': image_url,
                'caption': message,
                'parse_mode': 'Markdown'
            }
        else:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': channel_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
        
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            logger.info(f"✅ Сон для {bot_name} опубликован в канале")
            return True
        else:
            logger.error(f"❌ Ошибка публикации: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Ошибка при публикации: {e}")
        return False
