import os
import sys
import logging
sys.path.append('/root/ulibka_eco')
from core.bot_base import BotBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DentaiBot(BotBase):
    pass

if __name__ == '__main__':
    token = os.getenv('DENTIST_BOT_TOKEN')
    if not token:
        logger.error("DENTIST_BOT_TOKEN not set")
        sys.exit(1)
    bot = DentaiBot(token, "Помощник", "dentai")
    bot.run()
