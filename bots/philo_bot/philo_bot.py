#!/usr/bin/env python3
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('philo_bot')

QUOTES = [
    "Улыбка — это кривая, которая всё выпрямляет.",
    "Зубы даны человеку один раз, как и жизнь.",
    "Гигиена начинается с головы, а продолжается зубами.",
    "Стоматолог — это философ, только с бормашиной.",
    "Здоровые зубы — зеркало души."
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📚 Я бот-философ. Люблю порассуждать о зубах и жизни. Напиши мне что-нибудь!"
    )

async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text(f"📚 {random.choice(QUOTES)}")

def main():
    token = os.environ.get('PHILOSOPHER_BOT_TOKEN')
    if not token:
        logger.error("PHILOSOPHER_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Philo-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
