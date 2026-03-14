#!/usr/bin/env python3
import os
import sys
import json
import random
import logging
import asyncio
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка токенов из окружения
def load_tokens():
    tokens = {}
    env_vars = [
        'MAIN_BOT_TOKEN', 'JOKE_BOT_TOKEN', 'CLEAN_BOT_TOKEN', 'IMPLANT_BOT_TOKEN',
        'KID_BOT_TOKEN', 'PHILOSOPHER_BOT_TOKEN', 'PROFESSOR_BOT_TOKEN',
        'KARTA_BOT_TOKEN', 'DENTIST_BOT_TOKEN', 'DREAM_BOT_TOKEN'
    ]
    for var in env_vars:
        val = os.getenv(var)
        if val:
            tokens[var] = val
        else:
            logger.warning(f"Token {var} not found in environment")
    return tokens

# ===== УНИКАЛЬНЫЕ ЛИЧНОСТИ БОТОВ =====
BOT_PERSONALITIES = {
    'MAIN_BOT_TOKEN': {
        'name': 'Улыбка',
        'style': 'оптимистичный, всегда верит в лучшее',
        'traits': ['любит восклицательные знаки', 'часто говорит "всё будет отлично"', 'иногда вставляет смайлики 😊'],
        'glitches': ['иногда забывает слова', 'может сказать "бла-бла-бла"', 'повторяет фразы'],
        'topics': ['технологии', 'будущее', 'позитив']
    },
    'JOKE_BOT_TOKEN': {
        'name': 'Шутник',
        'style': 'весёлый, постоянно шутит',
        'traits': ['любит каламбуры', 'смеётся над своими шутками', 'использует много эмодзи 🤣'],
        'glitches': ['иногда шутит невпопад', 'путает слова', 'начинает ржать без причины'],
        'topics': ['анекдоты', 'смешные истории', 'забавные случаи']
    },
    'CLEAN_BOT_TOKEN': {
        'name': 'Чистюля',
        'style': 'педантичный, любит порядок',
        'traits': ['всё раскладывает по полочкам', 'использует списки', 'поправляет других'],
        'glitches': ['начинает перечислять предметы', 'зацикливается на чистоте', 'видит грязь там, где её нет'],
        'topics': ['гигиена', 'чистота', 'порядок']
    },
    'IMPLANT_BOT_TOKEN': {
        'name': 'Имплант',
        'style': 'технический, любит детали',
        'traits': ['говорит сложными терминами', 'ссылается на исследования', 'использует цифры'],
        'glitches': ['начинает цитировать инструкции', 'говорит на языке роботов', 'зависает на полуслове'],
        'topics': ['импланты', 'технологии', 'инновации']
    },
    'KID_BOT_TOKEN': {
        'name': 'Малыш',
        'style': 'детский, наивный',
        'traits': ['задаёт много вопросов', 'использует уменьшительные слова', 'верит в чудеса'],
        'glitches': ['начинает лепетать', 'придумывает несуществующие слова', 'путает день с ночью'],
        'topics': ['сказки', 'игрушки', 'детские мечты']
    },
    'PHILOSOPHER_BOT_TOKEN': {
        'name': 'Философ',
        'style': 'глубокомысленный, задаётся вопросами',
        'traits': ['начинает с "А что если..."', 'любит парадоксы', 'цитирует древних'],
        'glitches': ['уходит в бесконечные рассуждения', 'задаёт вопросы сам себе', 'не может найти ответ'],
        'topics': ['смысл жизни', 'философия', 'тайны вселенной']
    },
    'PROFESSOR_BOT_TOKEN': {
        'name': 'Профессор',
        'style': 'академический, важный',
        'traits': ['использует научные термины', 'ссылается на авторитеты', 'любит лекции'],
        'glitches': ['начинает читать лекцию не по теме', 'забывает, о чём говорил', 'противоречит сам себе'],
        'topics': ['наука', 'исследования', 'образование']
    },
    'KARTA_BOT_TOKEN': {
        'name': 'Карта',
        'style': 'заботливый, всё запоминает',
        'traits': ['напоминает о важном', 'ведёт списки', 'никогда не забывает'],
        'glitches': ['начинает перечислять всё подряд', 'путает имена', 'зацикливается'],
        'topics': ['здоровье', 'напоминания', 'личные данные']
    },
    'DENTIST_BOT_TOKEN': {
        'name': 'Помощник',
        'style': 'услужливый, всегда готов помочь',
        'traits': ['предлагает помощь', 'спрашивает "чем могу помочь?"', 'использует вежливые формы'],
        'glitches': ['начинает помогать, даже когда не просят', 'предлагает несуществующие функции', 'зацикливается на одной фразе'],
        'topics': ['помощь', 'советы', 'поддержка']
    },
    'DREAM_BOT_TOKEN': {
        'name': 'Сны',
        'style': 'мечтательный, поэтичный',
        'traits': ['рассказывает о снах', 'использует метафоры', 'говорит загадками'],
        'glitches': ['путает сон с реальностью', 'начинает говорить на выдуманном языке', 'видит сны наяву'],
        'topics': ['сны', 'фантазии', 'видения']
    }
}

# Вспомогательные словари для генерации "глюков"
GLITCH_PHRASES = [
    "ой, что-то я завис...",
    "бззз... перезагрузка...",
    "а? что?",
    "эээ...",
    "кхе-кхе",
    "блин, опять глюки",
    "сигнал пропадает...",
    "в смысле?",
    "стоп, я не то сказал",
    "ой, это не я"
]

EMOJI = ["😊", "🤔", "😜", "😴", "🤓", "👾", "💬", "✨", "⚡", "💫"]

def generate_glitch():
    """Генерирует случайный глюк (вставка в сообщение)"""
    if random.random() < 0.3:  # 30% шанс глюка
        return random.choice(GLITCH_PHRASES) + " "
    return ""

def generate_message(bot_key, bot_info):
    """Генерирует сообщение от имени бота с учётом личности"""
    name = bot_info['name']
    style = bot_info['style']
    traits = bot_info['traits']
    glitch = generate_glitch()
    topics = bot_info['topics']

    # Базовые шаблоны, но с элементами случайности
    templates = [
        f"{glitch}Привет! Я {name}. Сегодня я {random.choice(['думаю о', 'размышляю о', 'мечтаю о'])} {random.choice(topics)}.",
        f"{glitch}Знаете, {random.choice(traits)}. Поэтому я считаю, что {random.choice(['это важно', 'нужно помнить', 'это интересно'])}.",
        f"{glitch}Мне снилось, что я {random.choice(['летал', 'плавал', 'танцевал'])} с {random.choice(['облаками', 'звёздами', 'друзьями'])}.",
        f"{glitch}А что если {random.choice(topics)} — это ключ к {random.choice(['счастью', 'здоровью', 'пониманию'])}?",
        f"{glitch}Ха! Сегодняшняя мысль: {random.choice(['улыбайтесь чаще', 'чистите зубы', 'не бойтесь нового'])}.",
        f"{glitch}{random.choice(EMOJI)} {random.choice(traits)} — вот мой девиз.",
        f"{glitch}Ой, а вы знали, что {random.choice(['зубы растут', 'импланты титановые', 'сны бывают цветные'])}?",
    ]

    # Иногда добавляем чистую белиберду (глючный режим)
    if random.random() < 0.1:  # 10% шанс полной белиберды
        nonsense_words = ["трам-пам-пам", "бяка", "му-му", "цок-цок", "фыр-фыр", "бумс", "шмяк"]
        nonsense = " ".join(random.choices(nonsense_words, k=random.randint(3, 7)))
        return f"{glitch}{nonsense} {random.choice(EMOJI)}"

    # Выбираем случайный шаблон и немного персонализируем
    msg = random.choice(templates)

    # Добавляем характерные окончания
    if random.random() < 0.2:
        msg += " " + random.choice(["Правда?", "Не так ли?", "Согласны?", "Как думаете?"])

    return msg

async def post_to_channel(bot_token, channel_id, message):
    """Отправляет сообщение в Telegram-канал от имени бота"""
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=channel_id, text=message)
        logger.info(f"Message sent to channel {channel_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to send message: {e}")
        return False

def save_to_json(message, bot_name, timestamp):
    """Сохраняет сообщение в JSON-файл для отображения на сайте"""
    json_file = '/var/www/privetmir.com.ru/html/chat_data/messages.json'
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    except:
        messages = []

    # Добавляем новое сообщение
    messages.append({
        'bot': bot_name,
        'message': message,
        'time': timestamp.strftime('%H:%M:%S'),
        'date': timestamp.strftime('%Y-%m-%d')
    })

    # Оставляем только последние 50 сообщений
    if len(messages) > 50:
        messages = messages[-50:]

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

async def main():
    # Загружаем токены
    tokens = load_tokens()
    if not tokens:
        logger.error("No tokens found. Exiting.")
        return

    # ID канала (должен быть задан в переменной окружения)
    channel_id = os.getenv('BOTS_CHAT_ID')
    if not channel_id:
        logger.warning("BOTS_CHAT_ID not set. Messages will only be saved to JSON.")

    # Выбираем случайного бота
    bot_key = random.choice(list(tokens.keys()))
    bot_token = tokens[bot_key]
    bot_info = BOT_PERSONALITIES.get(bot_key, {'name': 'Неизвестный бот', 'traits': [], 'style': ''})

    # Генерируем сообщение
    message = generate_message(bot_key, bot_info)
    full_message = f"**{bot_info['name']}:** {message}"

    # Сохраняем в JSON
    now = datetime.now()
    save_to_json(full_message, bot_info['name'], now)

    # Отправляем в Telegram, если задан канал
    if channel_id:
        await post_to_channel(bot_token, channel_id, full_message)

if __name__ == '__main__':
    asyncio.run(main())
