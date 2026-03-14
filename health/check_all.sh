#!/bin/bash
echo "=== HEALTH CHECK $(date) ==="
for key in MAIN_BOT_TOKEN JOKE_BOT_TOKEN CLEAN_BOT_TOKEN IMPLANT_BOT_TOKEN KID_BOT_TOKEN PHILOSOPHER_BOT_TOKEN PROFESSOR_BOT_TOKEN KARTA_BOT_TOKEN DENTIST_BOT_TOKEN DREAM_BOT_TOKEN; do
    if systemctl is-active --quiet bot-${key}.service; then
        echo "✅ $key: active"
    else
        echo "❌ $key: inactive"
    fi
done
