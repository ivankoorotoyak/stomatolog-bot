#!/usr/bin/env python3
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('joke_bot')

JOKES = [
    "Встречаются два стоматолога: — Как жизнь? — Да так, тяну понемногу...",
    "— Доктор, у меня зубы жёлтые. — Носите коричневый галстук.",
    "— Доктор, у меня зуб болит. — А водку пробовали? — Нет. — Попробуйте, но петь перестанете.",
    "Зубная фея существует. Я её видел — она приходит за последними деньгами.",
    "— Почему стоматологи всегда весёлые? — Они тянут резину."
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🤣 Я бот-шутник! Отправь /joke или /анекдот, чтобы посмеяться."
    )

async def joke(update: Update, context: CallbackContext):
    await update.message.reply_text(f"🤣 {random.choice(JOKES)}")

def main():
    token = os.environ.get('JOKE_BOT_TOKEN')
    if not token:
        logger.error("JOKE_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("анекдот", joke))
    logger.info("✅ Joke-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
