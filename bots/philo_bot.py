import os
import sys
import logging
sys.path.append('/root/ulibka_eco')
from core.bot_base import BotBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhiloBot(BotBase):
    pass

if __name__ == '__main__':
    token = os.getenv('PHILOSOPHER_BOT_TOKEN')
    if not token:
        logger.error("PHILOSOPHER_BOT_TOKEN not set")
        sys.exit(1)
    bot = PhiloBot(token, "Философ", "philo")
    bot.run()
