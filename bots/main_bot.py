import os
import sys
import logging
sys.path.append('/root/ulibka_eco')
from core.bot_base import BotBase
from telegram.ext import CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainBot(BotBase):
    def setup_handlers(self):
        super().setup_handlers()
        self.application.add_handler(CommandHandler("info", self.info))
    
    async def info(self, update, context):
        await update.message.reply_text(
            "🤖 Я главный бот экосистемы «Улыбка».\n"
            "У нас есть и другие боты:\n"
            "@Ulibka_jokeBot — шутник\n"
            "@Ulibka_cleanBot — гигиена\n"
            "@Ulibka_implantBot — имплантология\n"
            "@Ulibka_kidBot — детский\n"
            "@Ulibka_philoBot — философ\n"
            "@Ulibka_profBot — для коллег\n"
            "@Stomkartabot — карта пациента\n"
            "@dentai_help_bot — врачебный помощник\n\n"
            "А ещё у нас есть 3D-вселенная: http://5.42.106.10"
        )

if __name__ == '__main__':
    token = os.getenv('MAIN_BOT_TOKEN')
    if not token:
        logger.error("MAIN_BOT_TOKEN not set")
        sys.exit(1)
    bot = MainBot(token, "Улыбка", "main")
    bot.run()
