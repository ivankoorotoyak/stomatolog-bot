import os
import json
import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logger = logging.getLogger(__name__)

class FootballBot:
    def __init__(self, token, bot_name, bot_data):
        self.token = token
        self.bot_name = bot_name
        self.data = bot_data
        self.health = True
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("card", self.card))
        self.application.add_handler(CommandHandler("thought", self.random_thought))
        self.application.add_handler(CommandHandler("health", self.health_check))
        self.application.add_handler(CallbackQueryHandler(self.button_click))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = (f"⚽ Привет! Я *{self.bot_name}*, играю на позиции *{self.data['position']}*.\n"
                f"Характер: {self.data['character']}\n"
                f"Особая фишка: {self.data['trick']}")
        keyboard = [
            [InlineKeyboardButton("📋 Карточка", callback_data="card")],
            [InlineKeyboardButton("💭 Случайная мысль", callback_data="thought")]
        ]
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    
    async def card(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        thoughts = random.sample(self.data['thoughts'], 3)
        text = (f"⚽ **{self.bot_name}**\n"
                f"*Позиция:* {self.data['position']}\n"
                f"*Характер:* {self.data['character']}\n\n"
                f"*Мысли вслух:*\n• " + "\n• ".join(thoughts))
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def random_thought(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        thought = random.choice(self.data['thoughts'])
        await update.message.reply_text(f"💭 {thought}")
    
    async def health_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ Я жив и здоров!")
    
    async def button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == "card":
            await self.card(update, context)
        elif query.data == "thought":
            await self.random_thought(update, context)
    
    async def run_async(self):
        """Асинхронный запуск (для использования в отдельной задаче)"""
        await self.application.initialize()
        await self.application.start()
        logger.info(f"Bot {self.bot_name} started")
        # Бесконечное ожидание с возможностью проверки здоровья
        while self.health:
            await asyncio.sleep(10)
        await self.application.stop()
    
    def stop(self):
        self.health = False
