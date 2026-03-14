#!/usr/bin/env python3
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kid_bot')

FACTS = [
    "Зубки нужно чистить 2 раза в день — утром и перед сном! 🪥",
    "У детей 20 молочных зубов, а у взрослых 32 постоянных!",
    "Зубная фея любит, когда дети чистят зубки!",
    "Чтобы зубки были крепкими, ешь творожок и пей молочко! 🥛",
    "Чистить зубки нужно 2 минутки — как любимая песенка!"
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🧸 Привет, малыш! Я расскажу про зубки. Напиши мне что-нибудь!"
    )

async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text(f"🧸 {random.choice(FACTS)}")

def main():
    token = os.environ.get('KID_BOT_TOKEN')
    if not token:
        logger.error("KID_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Kid-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
