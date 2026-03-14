import redis
import json
import threading
import time
from datetime import datetime

class QuantumChat:
    def __init__(self, bot_name, host='redis', port=6379):
        self.bot_name = bot_name
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        self.channel = 'quantum_bots_chat'
        self.listener_thread = None
        self.is_listening = False
        
    def publish_event(self, event_type, data):
        """Публикует событие от бота"""
        message = {
            'bot': self.bot_name,
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.redis_client.publish(self.channel, json.dumps(message, ensure_ascii=False))
        print(f"📤 [{self.bot_name}] опубликовал: {event_type}")
        
    def start_listening(self, callback):
        """Запускает прослушивание событий"""
        self.is_listening = True
        self.listener_thread = threading.Thread(target=self._listen, args=(callback,))
        self.listener_thread.daemon = True
        self.listener_thread.start()
        
    def _listen(self, callback):
        self.pubsub.subscribe(self.channel)
        for message in self.pubsub.listen():
            if not self.is_listening:
                break
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    if data['bot'] != self.bot_name:  # Не слушать свои сообщения
                        callback(data)
                except:
                    pass
                    
    def stop_listening(self):
        self.is_listening = False
        self.pubsub.unsubscribe()
