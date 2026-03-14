#!/usr/bin/env python3
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('stomka_bot')

INFO = [
    "Цифровая карта пациента — это удобно. Все данные под рукой.",
    "В карте можно хранить историю посещений, снимки, планы лечения.",
    "Электронная карта не теряется, в отличие от бумажной.",
    "Стоматологи видят всю историю лечения за минуту."
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🗺️ Я бот-карта. Расскажу про цифровые карты пациентов. Напиши мне!"
    )

async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text(f"🗺️ {random.choice(INFO)}")

def main():
    token = os.environ.get('KARTA_BOT_TOKEN')
    if not token:
        logger.error("KARTA_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Stomka-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
