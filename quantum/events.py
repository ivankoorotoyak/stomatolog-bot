import random
import json
import asyncio
from datetime import datetime
import aiohttp

QUANTUM_EVENTS = [
    {
        "name": "ball_pulse",
        "description": "⚽ Футбольный мяч пульсирует ярким светом!",
        "effect": "ball_scale_up",
        "duration": 2
    },
    {
        "name": "bot_blink",
        "description": "💡 Один из ботов начал мигать всеми цветами радуги!",
        "effect": "bot_rainbow",
        "duration": 3
    },
    {
        "name": "hole_sneeze",
        "description": "🌀 Чёрная дыра чихнула, из неё вылетели маленькие звёздочки!",
        "effect": "hole_sparkles",
        "duration": 1
    },
    {
        "name": "quantum_tangle",
        "description": "🔀 Связи между ботами запутались и стали разноцветными!",
        "effect": "lines_random_color",
        "duration": 4
    },
    {
        "name": "goal_scream",
        "description": "📢 Все боты одновременно закричали: ГООООЛ!",
        "effect": "bots_goal",
        "duration": 1
    },
    {
        "name": "ball_double",
        "description": "⚽⚽ Мяч разделился на два, и они запрыгали в разные стороны!",
        "effect": "ball_clone",
        "duration": 5
    },
    {
        "name": "gravity_shift",
        "description": "🌍 Гравитация изменилась — все боты подпрыгнули!",
        "effect": "bots_jump",
        "duration": 2
    },
    {
        "name": "thought_wave",
        "description": "💭 Мысли ботов стали видны прямо в воздухе!",
        "effect": "thought_bubbles",
        "duration": 3
    },
    {
        "name": "stadium_light",
        "description": "🏟️ Стадион зажёг прожекторы — стало светло как днём!",
        "effect": "ambient_light",
        "duration": 4
    },
    {
        "name": "fan_chant",
        "description": "🎶 Слышна кричалка болельщиков: 'Оле-оле-оле!'",
        "effect": "chant_audio",
        "duration": 2
    },
    {
        "name": "referee_whistle",
        "description": "📣 Судья дал свисток — матч продолжается!",
        "effect": "whistle",
        "duration": 1
    },
    {
        "name": "quantum_flip",
        "description": "🌀 Мяч и боты поменялись местами на мгновение!",
        "effect": "teleport_swap",
        "duration": 1
    }
]

async def quantum_loop():
    """Генерирует события и рассылает их через WebSocket (или сохраняет в JSON)"""
    # Здесь можно использовать Redis Pub/Sub или WebSocket
    while True:
        await asyncio.sleep(60)  # каждую минуту
        event = random.choice(QUANTUM_EVENTS)
        event['timestamp'] = datetime.now().isoformat()
        
        # Сохраняем для сайта
        try:
            with open('/var/www/privetmir.com.ru/html/quantum_event.json', 'w') as f:
                json.dump(event, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving quantum event: {e}")
        
        # Отправляем в лог
        print(f"⚡ QUANTUM EVENT: {event['name']} - {event['description']}")
        
        # Если есть веб-сокет сервер, можно отправить событие туда
        # async with aiohttp.ClientSession() as session:
        #     await session.post('http://localhost:8080/event', json=event)
