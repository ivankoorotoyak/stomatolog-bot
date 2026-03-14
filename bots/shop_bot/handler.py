#!/usr/bin/env python3
import logging
import os
import sys
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

sys.path.append('/root/ulibka_eco')
from bots.shop_bot.demo_catalog import (
    PRODUCTS, get_product_by_id, get_products_by_category, 
    get_all_categories, format_product_text, get_popular_products,
    search_products
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('shop_bot')

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛍️ Каталог", callback_data="menu_catalog"),
         InlineKeyboardButton("📋 Категории", callback_data="menu_categories")],
        [InlineKeyboardButton("🔥 Популярное", callback_data="menu_popular"),
         InlineKeyboardButton("🔍 Поиск", callback_data="menu_search")],
        [InlineKeyboardButton("🆘 Помощь", callback_data="menu_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def start_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        f"🛍️ *Добро пожаловать!*\n\nПривет, {user.first_name}!",
        reply_markup=main_menu_keyboard(),
        parse_mode='Markdown'
    )

def menu_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    
    if data == "menu_catalog":
        show_catalog(query)
    elif data == "menu_categories":
        show_categories(query)
    elif data == "menu_popular":
        show_popular(query)
    elif data == "menu_search":
        show_search(query)
    elif data == "menu_help":
        show_help(query)
    elif data.startswith('product_'):
        show_product(query)
    elif data.startswith('category_'):
        show_category_products(query)
    elif data == "back_to_main":
        query.edit_message_text("🛍️ *Главное меню*", reply_markup=main_menu_keyboard(), parse_mode='Markdown')

def show_catalog(query):
    keyboard = []
    for p in PRODUCTS[:5]:
        keyboard.append([InlineKeyboardButton(f"{p['name']} - {p['price']} ₽", callback_data=f"product_{p['id']}")])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    query.edit_message_text("🛒 *Каталог*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def show_categories(query):
    cats = get_all_categories()
    keyboard = [[InlineKeyboardButton(c.capitalize(), callback_data=f"category_{c}")] for c in cats]
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    query.edit_message_text("📋 *Категории*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def show_popular(query):
    products = get_popular_products(3)
    keyboard = [[InlineKeyboardButton(f"{p['name']} - {p['price']} ₽", callback_data=f"product_{p['id']}")] for p in products]
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")])
    query.edit_message_text("🔥 *Популярное*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def show_search(query):
    query.edit_message_text(
        "🔍 *Поиск*\n\nПросто напиши название товара",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")]]),
        parse_mode='Markdown'
    )

def show_product(query):
    pid = int(query.data.split('_')[1])
    p = get_product_by_id(pid)
    if p:
        text = format_product_text(p)
        keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")]]
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def show_category_products(query):
    cat = query.data.split('_')[1]
    products = get_products_by_category(cat)
    keyboard = [[InlineKeyboardButton(f"{p['name']} - {p['price']} ₽", callback_data=f"product_{p['id']}")] for p in products[:5]]
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="menu_categories")])
    query.edit_message_text(f"📦 *{cat.capitalize()}*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def show_help(query):
    query.edit_message_text(
        "🆘 *Помощь*\n\n/start - главное меню",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")]]),
        parse_mode='Markdown'
    )

def text_handler(update: Update, context: CallbackContext):
    query = update.message.text
    results = search_products(query)
    if not results:
        update.message.reply_text("😕 Ничего не найдено. Попробуйте /start")
        return
    keyboard = [[InlineKeyboardButton(f"{p['name']} - {p['price']} ₽", callback_data=f"product_{p['id']}")] for p in results[:5]]
    update.message.reply_text(f"🔍 *Результаты* ({len(results)})", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

def help_handler(update: Update, context: CallbackContext):
    update.message.reply_text("🆘 *Помощь*\n\n/start - главное меню", parse_mode='Markdown')

def main():
    token = os.environ.get('SHOP_BOT_TOKEN')
    if not token:
        logger.error("Токен не найден")
        return
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("help", help_handler))
    dp.add_handler(CallbackQueryHandler(menu_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))
    logger.info("✅ Бот запущен")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
