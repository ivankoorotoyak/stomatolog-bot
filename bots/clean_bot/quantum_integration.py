import sys
sys.path.append('/root/ulibka_eco')
from core.redis_chat.quantum_chat import QuantumChat
import random

quantum = QuantumChat('clean-bot')

def handle_quantum_event(event):
    """Реагирует на события других ботов"""
    if event['type'] == 'user_question':
        question = event['data'].get('question', '')
        if 'чувствительность' in question:
            quantum.publish_event('bot_comment', {
                'text': '🧼 Я как раз знаю отличные пасты для чувствительных зубов!',
                'original_bot': event['bot']
            })
    elif event['type'] == 'bot_comment':
        if event['data'].get('original_bot') == 'clean-bot':
            return  # Не отвечать на комментарии про себя
        print(f"📩 clean-bot услышал: {event['data']['text']}")

# Запускаем прослушивание
quantum.start_listening(handle_quantum_event)
