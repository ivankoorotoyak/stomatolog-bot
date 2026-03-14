#!/usr/bin/env python3
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('plus_bot')

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("😄 Шутник", url="https://t.me/Ulibka_jokeBot"),
         InlineKeyboardButton("🧸 Малыш", url="https://t.me/Ulibka_kidBot")],
        [InlineKeyboardButton("🦷 Имплант", url="https://t.me/Ulibka_implantBot"),
         InlineKeyboardButton("🧼 Гигиена", url="https://t.me/Ulibka_cleanBot")],
        [InlineKeyboardButton("📚 Философ", url="https://t.me/Ulibka_philoBot"),
         InlineKeyboardButton("👨‍🏫 Профессор", url="https://t.me/Ulibka_profBot")],
        [InlineKeyboardButton("🗺️ Карта", url="https://t.me/Stomkartabot"),
         InlineKeyboardButton("🆘 Помощник", url="https://t.me/dentai_help_bot")],
        [InlineKeyboardButton("🛒 Магазин", url="https://t.me/shop_ulikabot"),
         InlineKeyboardButton("🌙 Сны", url="https://t.me/ulybka_plus_dreams")]
    ]
    await update.message.reply_text(
        "🌟 *Вселенная Улыбка*\n\n"
        "Выбери бота, с которым хочешь пообщаться:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

def main():
    token = os.environ.get('PLUS_BOT_TOKEN')
    if not token:
        logger.error("PLUS_BOT_TOKEN не задан")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("✅ Plus-bot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
