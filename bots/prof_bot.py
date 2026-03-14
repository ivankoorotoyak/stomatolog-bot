import os
import sys
import logging
sys.path.append('/root/ulibka_eco')
from core.bot_base import BotBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfBot(BotBase):
    pass

if __name__ == '__main__':
    token = os.getenv('PROFESSOR_BOT_TOKEN')
    if not token:
        logger.error("PROFESSOR_BOT_TOKEN not set")
        sys.exit(1)
    bot = ProfBot(token, "Профессор", "prof")
    bot.run()
