import os
import json
import subprocess
from datetime import datetime

BOT_TEMPLATES = {
    'clean': {
        'name': 'Гигиенист',
        'description': 'Бот для советов по гигиене полости рта',
        'price_stars': 5000,
        'price_rub': 5000,
        'setup_time': '5 минут'
    },
    'joke': {
        'name': 'Шутник',
        'description': 'Бот с анекдотами про стоматологию',
        'price_stars': 3000,
        'price_rub': 3000,
        'setup_time': '5 минут'
    },
    'plus': {
        'name': 'Главный бот',
        'description': 'Центральный бот с меню всех остальных',
        'price_stars': 8000,
        'price_rub': 8000,
        'setup_time': '10 минут'
    },
    'full_pack': {
        'name': 'Вселенная Улыбка (полный пакет)',
        'description': 'Все 10 ботов + дашборд + Redis + автозапуск',
        'price_stars': 50000,
        'price_rub': 50000,
        'setup_time': '30 минут'
    }
}

def deploy_bot_for_client(bot_type, client_domain, client_email):
    """Разворачивает копию бота для клиента на отдельном сервере"""
    # В реальности здесь будет вызов API облачного провайдера
    # Сейчас просто логируем
    order = {
        'bot_type': bot_type,
        'domain': client_domain,
        'email': client_email,
        'ordered_at': datetime.now().isoformat(),
        'status': 'pending'
    }
    
    # Сохраняем заказ
    orders_file = '/root/ulibka_eco/dashboard/shop/orders.json'
    if os.path.exists(orders_file):
        with open(orders_file, 'r') as f:
            orders = json.load(f)
    else:
        orders = []
    
    orders.append(order)
    with open(orders_file, 'w') as f:
        json.dump(orders, f, indent=2)
    
    return order
