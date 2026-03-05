#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен – обязательно должен называться TELEGRAM_BOT_TOKEN в .env
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не найден! Проверьте файл .env")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ---------- Хэндлеры ----------
@dp.message(Command('start'))
async def cmd_start(message: Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"👋 Привет, {user_name}!\n"
        "Я бот стоматологии «Улыбка+» (г. Острогожск).\n"
        "Наш девиз: «Лечим с заботой, дарим улыбки!» 😊\n"
        "Доступные команды: /help"
    )

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        "📋 Список команд:\n"
        "/start - Начало работы\n"
        "/help - Эта справка\n"
        "/info - Контактная информация и адрес"
    )

@dp.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer(
        "🦷 Стоматология «Улыбка+»\n"
        "📍 Адрес: г. Острогожск, ул. Ленина, 41\n"
        "📞 Телефон для справок и записи: +7 (47375) 4-64-61\n"
        "🕒 Часы работы: уточняйте по телефону\n\n"
        "✨ Наш девиз: «Лечим с заботой, дарим улыбки!»"
    )

@dp.message()
async def echo_message(message: Message):
    await message.answer(f"Вы написали: {message.text}")

# ---------- Запуск ----------
async def main():
    logging.info("🚀 Бот для стоматологии «Улыбка+» запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("⏹ Бот остановлен")
