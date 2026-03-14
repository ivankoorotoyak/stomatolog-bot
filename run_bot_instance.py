#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import logging
import signal
sys.path.append('/root/ulibka_eco')
from core.bot_base import FootballBot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'/root/ulibka_eco/logs/{sys.argv[1]}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    token_key = sys.argv[1]
    token = os.getenv(token_key)
    if not token:
        logger.error(f"Token {token_key} not found")
        sys.exit(1)
    
    # Загружаем данные ботов
    with open('/root/ulibka_eco/data/bots_data.json', 'r', encoding='utf-8') as f:
        bots_data = json.load(f)
    
    if token_key not in bots_data:
        logger.error(f"No data for {token_key}")
        sys.exit(1)
    
    bot_data = bots_data[token_key]
    bot = FootballBot(token, bot_data['name'], bot_data)
    
    # Обработка сигналов для graceful shutdown
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop.set_result, None)
    
    # Запуск бота асинхронно
    bot_task = asyncio.create_task(bot.run_async())
    
    # Ждём сигнала остановки
    await stop
    logger.info("Stopping bot...")
    bot.stop()
    await bot_task

if __name__ == '__main__':
    asyncio.run(main())
