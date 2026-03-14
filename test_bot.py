import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("✅ Загружаем токен...")
token = os.getenv('MAIN_BOT_TOKEN')
if not token:
    print("❌ MAIN_BOT_TOKEN не найден в окружении!")
    print("🔍 Текущие переменные окружения:")
    for key in os.environ.keys():
        if 'TOKEN' in key:
            print(f"  {key}={os.environ[key][:10]}...")
    sys.exit(1)

print(f"✅ Токен загружен: {token[:10]}...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я тестовый бот!')

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    print("✅ Бот запускается...")
    app.run_polling()

if __name__ == '__main__':
    main()
