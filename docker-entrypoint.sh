#!/bin/bash
BOT_NAME=${BOT_NAME:-stars}
TOKEN_VAR="${BOT_NAME^^}_BOT_TOKEN"
TOKEN=${!TOKEN_VAR}
[ -z "$TOKEN" ] && { echo "❌ Нет токена"; exit 1; }
export ${TOKEN_VAR}="$TOKEN"
echo "🚀 Запуск $BOT_NAME"
cd /app/bots/${BOT_NAME}_bot
python ${BOT_NAME}_bot.py
