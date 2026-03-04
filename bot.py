import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from cloud_model import ask_cloud_model

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Здравствуйте! Я – консультант стоматологии «Улыбка+». "
        "Задайте любой вопрос о здоровье зубов, гигиене или лечении. "
        "Я постараюсь дать полезную информацию, основанную на экспертизе наших врачей.\n\n"
        "⚠️ Помните: мои ответы носят справочный характер и не заменяют очный приём."
    )

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_cloud_model(message.text)
    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())