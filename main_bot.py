#!/usr/bin/env python3
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import chromadb
from sentence_transformers import SentenceTransformer
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
API_KEY = os.getenv("API_KEY")
YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
CHROMA_DIR = "/root/projects/stomatolog/chroma_db"

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection("stomatology_knowledge")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

def search_knowledge(query, top_k=3):
    query_emb = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    return results['documents'][0] if results['documents'] else []

async def ask_gpt_with_context(user_message):
    context_chunks = await asyncio.to_thread(search_knowledge, user_message)
    if context_chunks:
        context = "\n\n".join(context_chunks)
        system_prompt = f"Ты — стоматолог-консультант клиники «Улыбка+». Отвечай на основе следующих материалов. Если информации недостаточно, честно скажи об этом.\n\nМатериалы:\n{context}"
    else:
        system_prompt = "Ты — стоматолог-консультант. Ответь на вопрос, а если не знаешь, предложи обратиться к врачу."

    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": 1000},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": user_message}
        ]
    }
    resp = requests.post(YANDEX_GPT_URL, headers=headers, json=payload, timeout=10)
    if resp.status_code == 200:
        return resp.json()["result"]["alternatives"][0]["message"]["text"]
    else:
        return f"Ошибка YandexGPT: {resp.status_code}"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Здравствуйте! Я — консультант стоматологии «Улыбка+». "
        "Задайте любой вопрос о здоровье зубов, и я постараюсь помочь."
    )

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_gpt_with_context(message.text)
    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())