import sys
sys.path.append('/root/ulibka_eco')
from core.redis_chat.quantum_chat import QuantumChat
import random

quantum = QuantumChat('joke-bot')

JOKES = [
    "Встречаются два стоматолога...",
    "— Доктор, у меня зубы жёлтые. — Носите коричневый галстук!",
    "Зубная фея существует. Я её видел!"
]

def handle_quantum_event(event):
    if event['type'] == 'bot_comment':
        # Шутим в ответ на любой комментарий
        quantum.publish_event('bot_joke', {
            'text': random.choice(JOKES),
            'original_bot': event['bot']
        })

quantum.start_listening(handle_quantum_event)
