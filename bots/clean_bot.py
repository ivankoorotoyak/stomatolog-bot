import os
import sys
import random
import logging
sys.path.append('/root/ulibka_eco')
from core.bot_base import BotBase
from telegram.ext import CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CleanBot(BotBase):
    def setup_handlers(self):
        super().setup_handlers()
        self.application.add_handler(CommandHandler("hygiene", self.hygiene))
        self.application.add_handler(CommandHandler("совет", self.hygiene))
    
    async def hygiene(self, update, context):
        try:
            with open("/root/ulibka_eco/data/hygiene_tips.txt", "r", encoding="utf-8") as f:
                tips = f.readlines()
                tip = random.choice(tips).strip()
            await update.message.reply_text(f"💡 Гигиенический совет:\n\n{tip}")
        except Exception as e:
            logger.error(f"Error: {e}")
            await update.message.reply_text("😕 Не могу дать совет прямо сейчас")

if __name__ == '__main__':
    token = os.getenv('CLEAN_BOT_TOKEN')
    if not token:
        logger.error("CLEAN_BOT_TOKEN not set")
        sys.exit(1)
    bot = CleanBot(token, "Чистюля", "clean")
    bot.run()
