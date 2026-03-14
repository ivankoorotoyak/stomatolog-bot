import os
import sys
import random
import logging
sys.path.append('/root/ulibka_eco')
from core.bot_base import BotBase
from telegram.ext import CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JokeBot(BotBase):
    def setup_handlers(self):
        super().setup_handlers()
        self.application.add_handler(CommandHandler("joke", self.joke))
        self.application.add_handler(CommandHandler("анекдот", self.joke))
    
    async def joke(self, update, context):
        jokes = [
            "Встречаются два стоматолога: — Как жизнь? — Да так, тяну понемногу...",
            "— Доктор, у меня зубы жёлтые. Что делать? — Носите коричневый галстук.",
            "Стоматолог — пациенту: — Не бойтесь, больно не будет! Пациент: — А вы уже лечили? — Нет, я в цирке клоуном работал.",
            "— Доктор, у меня зуб болит. — А вы пробовали водку? — Нет, а поможет? — Не знаю, но петь перестанете точно."
        ]
        await update.message.reply_text(random.choice(jokes))

if __name__ == '__main__':
    token = os.getenv('JOKE_BOT_TOKEN')
    if not token:
        logger.error("JOKE_BOT_TOKEN not set")
        sys.exit(1)
    bot = JokeBot(token, "Шутник", "joke")
    bot.run()
