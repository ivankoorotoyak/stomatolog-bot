#!/usr/bin/env python3
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dentai_bot')

TIPS = [
    "Я помогу найти информацию о зубах и лечении.",
    "Спроси меня про гигиену, импланты или детские зубы.",
    "Могу подсказать, где читать про стоматологию.",
    "Всегда рад помочь!"
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🆘 Я бот-помощник. Спрашивай что угодно о зубах — поищу информацию!"
    )

async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text(f"🆘 {random.choice(TIPS)}")

def main():
    token = os.environ.get('DENTIST_BOT_TOKEN')
    if not token:
        logger.error("DENTIST_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Dentai-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
