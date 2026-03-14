#!/usr/bin/env python3
"""
Каталог товаров с партнёрскими ссылками
"""

PRODUCTS = [
    {
        "id": 1,
        "name": "Электрическая зубная щётка SonicPro",
        "description": "Профессиональная чистка с трёхмерным действием. 3 режима, таймер 2 минуты.",
        "price": 3990,
        "category": "гигиена",
        "url": "https://www.ozon.ru/product/123456789",
        "marketplace": "Ozon"
    },
    {
        "id": 2,
        "name": "Ирригатор AquaJet",
        "description": "Для идеальной чистки межзубных промежутков. 5 режимов, объём резервуара 600 мл.",
        "price": 5490,
        "category": "гигиена",
        "url": "https://www.wildberries.ru/catalog/987654321",
        "marketplace": "Wildberries"
    },
    {
        "id": 3,
        "name": "Отбеливающие полоски WhiteLight",
        "description": "Видимое отбеливание за 7 дней. Курс на 28 применений.",
        "price": 2490,
        "category": "отбеливание",
        "url": "https://ozon.ru/product/456789123",
        "marketplace": "Ozon"
    },
    {
        "id": 4,
        "name": "Зубная паста Professional Repair",
        "description": "Восстанавливает эмаль, защищает от кариеса. С фтором и кальцием.",
        "price": 890,
        "category": "гигиена",
        "url": "https://www.wildberries.ru/catalog/321654987",
        "marketplace": "Wildberries"
    },
    {
        "id": 5,
        "name": "Набор межзубных ёршиков",
        "description": "5 размеров, для идеальной чистки труднодоступных мест.",
        "price": 690,
        "category": "гигиена",
        "url": "https://ozon.ru/product/789123456",
        "marketplace": "Ozon"
    }
]

def get_product_by_id(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None

def get_products_by_category(category):
    return [p for p in PRODUCTS if p["category"] == category]

def get_all_categories():
    return list(set(p["category"] for p in PRODUCTS))

def format_product_text(product):
    return f"""🦷 *{product['name']}*
{product['description']}

💰 Цена: {product['price']} ₽

🛒 *Где купить:* [{product['marketplace']}]({product['url']})

_Это общая рекомендация. Товар есть в аптеках и на маркетплейсах._"""

def get_popular_products(limit=3):
    return PRODUCTS[:limit]

def search_products(query):
    query = query.lower()
    return [p for p in PRODUCTS if query in p["name"].lower() or query in p["description"].lower()]
