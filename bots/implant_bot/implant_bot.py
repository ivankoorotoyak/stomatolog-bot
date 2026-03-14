#!/usr/bin/env python3
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('implant_bot')

TIPS = [
    "Импланты — это новые корни для зубов. Они ставятся вместо удалённых.",
    "Импланты делают из титана — он хорошо приживается в кости.",
    "После установки импланта нужно ждать 3-6 месяцев для приживления.",
    "Импланты служат 20-30 лет при правильном уходе.",
    "Ухаживать за имплантами нужно как за своими зубами."
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🦷 Я бот-имплантолог. Расскажу про импланты. Просто напиши мне!"
    )

async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text(
        f"🦷 {random.choice(TIPS)}\n\n_Общая информация, не консультация._",
        parse_mode='Markdown'
    )

def main():
    token = os.environ.get('IMPLANT_BOT_TOKEN')
    if not token:
        logger.error("IMPLANT_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Implant-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
