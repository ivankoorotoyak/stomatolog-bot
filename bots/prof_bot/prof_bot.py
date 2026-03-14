#!/usr/bin/env python3
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('prof_bot')

FACTS = [
    "Знаете ли вы, что эмаль — самая твёрдая ткань в организме?",
    "Исследования показывают: чистка зубов снижает риск сердечных заболеваний.",
    "Фтор в пасте укрепляет эмаль и защищает от кариеса.",
    "Зубную щётку нужно менять каждые 3 месяца.",
    "Ирригатор удаляет до 99% налёта в труднодоступных местах."
]

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "👨‍🏫 Я бот-профессор. Расскажу научные факты о зубах. Задавай вопросы!"
    )

async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text(f"👨‍🏫 {random.choice(FACTS)}")

def main():
    token = os.environ.get('PROFESSOR_BOT_TOKEN')
    if not token:
        logger.error("PROFESSOR_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Prof-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
