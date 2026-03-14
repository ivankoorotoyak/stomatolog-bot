#!/usr/bin/env python3
import os
import sqlite3
import subprocess
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DB_PATH = "/var/lib/ulibka/ulibka.db"

def get_stats():
    stats = {
        'total_dreams': 0,
        'dreams_with_images': 0,
        'total_purchases': 0,
        'total_stars': 0,
        'total_users': 0,
        'bots_status': {},
        'recent_dreams': [],
        'recent_purchases': [],
        'chart_data': [0, 0, 0, 0, 0, 0, 0]
    }
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Таблицы
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [t[0] for t in tables]
        
        if 'dreams' in table_names:
            stats['total_dreams'] = cursor.execute("SELECT COUNT(*) FROM dreams").fetchone()[0]
            stats['dreams_with_images'] = cursor.execute("SELECT COUNT(*) FROM dreams WHERE image_url IS NOT NULL").fetchone()[0]
            
            dreams = cursor.execute(
                "SELECT bot_name, dream_text, created_at FROM dreams ORDER BY id DESC LIMIT 5"
            ).fetchall()
            for d in dreams:
                stats['recent_dreams'].append({
                    'bot': d[0],
                    'text': d[1][:50] + '...',
                    'time': d[2]
                })
            
            for i in range(7):
                day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                count = cursor.execute(
                    "SELECT COUNT(*) FROM dreams WHERE DATE(created_at) = ?",
                    (day,)
                ).fetchone()[0]
                stats['chart_data'][6-i] = count
        
        if 'purchases' in table_names:
            stats['total_purchases'] = cursor.execute("SELECT COUNT(*) FROM purchases").fetchone()[0]
            total = cursor.execute("SELECT SUM(stars_count) FROM purchases").fetchone()[0]
            stats['total_stars'] = total if total else 0
            
            purchases = cursor.execute(
                "SELECT user_id, stars_count, created_at FROM purchases ORDER BY id DESC LIMIT 5"
            ).fetchall()
            for p in purchases:
                stats['recent_purchases'].append({
                    'user': p[0],
                    'stars': p[1],
                    'time': p[2]
                })
        
        conn.close()
    except:
        pass
    
    # Статус ботов
    bots = ['plus', 'joke', 'clean', 'implant', 'kid', 'philo', 'prof', 'stomka', 'dentai', 'shop', 'stars']
    for bot in bots:
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', f'{bot}-bot.service'],
                capture_output=True,
                text=True
            )
            status = result.stdout.strip()
            stats['bots_status'][bot] = 'active' if status == 'active' else 'inactive'
        except:
            stats['bots_status'][bot] = 'inactive'
    
    return stats

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

# ============================================
# МАГАЗИН БОТОВ
# ============================================
@app.route('/api/shop/products')
def shop_products():
    return jsonify(BOT_TEMPLATES)

@app.route('/api/shop/order', methods=['POST'])
def shop_order():
    data = request.json
    bot_type = data.get('bot_type')
    client_domain = data.get('domain')
    client_email = data.get('email')
    
    if not bot_type or not client_domain or not client_email:
        return jsonify({'error': 'Missing data'}), 400
    
    order = deploy_bot_for_client(bot_type, client_domain, client_email)
    return jsonify(order)
