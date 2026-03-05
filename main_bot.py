import os
import json
import logging
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
API_KEY = os.getenv("API_KEY")
YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# Инициализация векторной базы
CHROMA_DIR = "/root/projects/stomatolog/chroma_db"
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection("stomatology_knowledge")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

logging.basicConfig(level=logging.INFO)

def search_knowledge(query, top_k=3):
    query_emb = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    if results['documents']:
        return results['documents'][0]
    return []

def ask_gpt_with_context(user_message):
    context_chunks = search_knowledge(user_message)
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

def handler(event, context):
    try:
        update = json.loads(event['body'])
        if 'message' not in update:
            return {'statusCode': 200, 'body': json.dumps({'ok': True})}
        msg = update['message']
        chat_id = msg['chat']['id']
        user_text = msg.get('text', '')
        if not user_text:
            return {'statusCode': 200, 'body': json.dumps({'ok': True})}
        answer = ask_gpt_with_context(user_text)
        send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        send_data = {'chat_id': chat_id, 'text': answer}
        requests.post(send_url, json=send_data)
        return {'statusCode': 200, 'body': json.dumps({'ok': True})}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}