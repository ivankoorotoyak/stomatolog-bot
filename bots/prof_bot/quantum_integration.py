import sys
sys.path.append('/root/ulibka_eco')
from core.redis_chat.quantum_chat import QuantumChat

quantum = QuantumChat('prof-bot')

FACTS = [
    "Исследования показывают: чувствительность зубов связана с эмалью!",
    "Знаете ли вы, что фтор укрепляет зубы на 40%?",
    "По статистике, 70% людей чистят зубы неправильно."
]

def handle_quantum_event(event):
    if event['type'] == 'bot_comment':
        # Добавляем научный факт
        quantum.publish_event('scientific_fact', {
            'text': random.choice(FACTS),
            'original_bot': event['bot']
        })

quantum.start_listening(handle_quantum_event)
