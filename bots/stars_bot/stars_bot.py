#!/usr/bin/env python3
"""
Бот для демонстрации оплаты через Telegram Stars
"""
import logging
import sqlite3
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('stars_bot')

# Токен бота (прямо в коде)
TOKEN = "8782019622:AAF62zThjbtbo8mBnTpa9H2zZJjHBeRJR1E"
BOT_USERNAME = "@stars_ulibkabot"
DB_PATH = "/var/lib/ulibka/ulibka.db"

def init_db():
    """Создаёт таблицу для заказов, если её нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            stars_count INTEGER,
            status TEXT,
            payment_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Инициализация
init_db()

async def start(update: Update, context: CallbackContext):
    """Приветственное сообщение с кнопкой для покупки"""
    keyboard = [
        [InlineKeyboardButton("⭐ 100 Stars", callback_data="buy_100"),
         InlineKeyboardButton("⭐ 500 Stars", callback_data="buy_500")],
        [InlineKeyboardButton("⭐ 1000 Stars", callback_data="buy_1000"),
         InlineKeyboardButton("⭐ 2500 Stars", callback_data="buy_2500")],
        [InlineKeyboardButton("📊 Баланс", callback_data="balance")]
    ]
    await update.message.reply_text(
        "🌟 *Telegram Stars Shop*\n\n"
        "Привет! Здесь ты можешь купить Telegram Stars для поддержки проекта.\n\n"
        "Stars можно потратить на:\n"
        "• 💎 Премиум-функции в наших ботах\n"
        "• 🎁 Уникальные подарки\n"
        "• 🌙 Эксклюзивные сны ботов\n\n"
        "👇 Выбери сумму:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: CallbackContext):
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "balance":
        await show_balance(update, context)
        return
    
    if data.startswith('buy_'):
        stars = int(data.split('_')[1])
        
        # Создаём счёт для оплаты Stars
        prices = [LabeledPrice(label="Telegram Stars", amount=stars)]
        payload = f"stars_{stars}_{query.from_user.id}"
        
        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title=f"Покупка {stars} Stars",
            description=f"Пополнение баланса на {stars} Stars",
            payload=payload,
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter="stars_payment"
        )

async def show_balance(update: Update, context: CallbackContext):
    """Показывает историю покупок пользователя"""
    user_id = update.effective_user.id
    
    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    purchases = cursor.execute(
        "SELECT stars_count, created_at FROM purchases WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user_id,)
    ).fetchall()
    
    total = cursor.execute(
        "SELECT SUM(stars_count) FROM purchases WHERE user_id = ?",
        (user_id,)
    ).fetchone()[0] or 0
    conn.close()
    
    if not purchases:
        await message.reply_text("У тебя пока нет покупок.")
        return
    
    text = f"📊 *Твой баланс:* ⭐ {total} Stars\n\n📝 *Последние покупки:*\n"
    for p in purchases:
        text += f"  • {p[0]} Stars — {p[1]}\n"
    
    await message.reply_text(text, parse_mode='Markdown')

async def pre_checkout_handler(update: Update, context: CallbackContext):
    """Проверка перед оплатой"""
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment_handler(update: Update, context: CallbackContext):
    """Обработка успешной оплаты"""
    payment = update.message.successful_payment
    stars = payment.total_amount
    user_id = update.effective_user.id
    payment_id = payment.telegram_payment_charge_id
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO purchases (user_id, stars_count, status, payment_id) VALUES (?, ?, ?, ?)",
        (user_id, stars, 'paid', payment_id)
    )
    conn.commit()
    conn.close()
    
    await update.message.reply_text(
        f"✅ *Спасибо за поддержку!*\n\n"
        f"Ты пополнил баланс на *{stars} Stars*\n\n"
        f"Твой вклад помогает развивать Вселенную Улыбка! 💙",
        parse_mode='Markdown'
    )

async def balance_command(update: Update, context: CallbackContext):
    """Команда /balance"""
    await show_balance(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))
    
    logger.info("✅ Stars-bot запущен")
    print(f"✅ Бот {BOT_USERNAME} запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()
