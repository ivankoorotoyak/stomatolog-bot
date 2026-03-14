#!/usr/bin/env python3
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)

class BaseBot:
    def __init__(self, token, bot_name):
        self.token = token
        self.bot_name = bot_name
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
    
    async def start(self, update: Update, context: CallbackContext):
        await update.message.reply_text(
            f"🤖 Привет! Я бот *{self.bot_name}*.\n"
            f"Я часть Вселенной Улыбка. Скоро я научусь чему-то интересному!\n\n"
            f"А пока загляни к другим: @Ulibka_plusBot",
            parse_mode='Markdown'
        )
    
    def run(self):
        logging.info(f"✅ {self.bot_name}-bot запущен")
        self.app.run_polling()
