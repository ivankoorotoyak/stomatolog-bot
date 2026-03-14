#!/usr/bin/env python3
"""
Бот-гигиенист — стабильная версия
"""
import logging
import os
import sys
sys.path.append('/root/ulibka_eco')
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Заглушка для модуля гигиены (если нет модуля)
try:
    from modules.hygiene import get_hygiene_advice
except ImportError:
    def get_hygiene_advice(text):
        return "🦷 Рекомендация: используйте мягкую щётку и пасту с фтором."

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('clean_bot')

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("🦷 Гигиена", callback_data="hygiene_menu")]]
    await update.message.reply_text(
        f"🪥 Привет, {user.first_name}! Я бот-гигиенист.\n\n"
        "Я помогу с выбором средств гигиены.\n\n"
        "⚠️ *Важно*: Я не врач, не ставлю диагнозы.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🦷 Опишите проблему:\nчувствительность / кровоточивость / налёт / запах",
        parse_mode='Markdown'
    )
    context.user_data['hygiene_mode'] = True

async def handle_message(update: Update, context: CallbackContext):
    if context.user_data.get('hygiene_mode'):
        text = update.message.text
        advice = get_hygiene_advice(text)
        await update.message.reply_text(advice, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("🆘 /start - начать")

def main():
    token = os.environ.get('CLEAN_BOT_TOKEN')
    if not token:
        logger.error("Токен не задан")
        return
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
