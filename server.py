from flask import Flask
import os
import subprocess
import threading
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот Головина Романа работает! Telegram: @UCHEBAutk_bot"

@app.route('/health')
def health():
    return "OK"

@app.route('/test-yandex')
def test_yandex():
    try:
        from yandex_gpt import yandex_gpt
        status = "настроен" if yandex_gpt.is_configured() else "не настроен"
        return f"Yandex GPT: {status}"
    except Exception as e:
        return f"Error: {e}"

def run_bot():
    """Запуск бота с улучшенной обработкой ошибок"""
    time.sleep(10)
    
    while True:
        try:
            logger.info("🔄 Запускаем бота...")
            
            # Проверяем наличие необходимых переменных окружения
            required_vars = ['BOT_TOKEN', 'YANDEX_GPT_API_KEY', 'YANDEX_FOLDER_ID']
            missing_vars = [var for var in required_vars if not os.environ.get(var)]
            
            if missing_vars:
                logger.error(f"❌ Отсутствуют переменные окружения: {missing_vars}")
                time.sleep(60)
                continue
            
            # Запускаем бота
            process = subprocess.run(
                ['python', 'bot.py'], 
                capture_output=True, 
                text=True,
                timeout=300
            )
            
            if process.stdout:
                logger.info(f"Бот: {process.stdout}")
            if process.stderr:
                logger.error(f"Ошибки бота: {process.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.info("⏰ Бот работает... перезапускаем через 30 секунд")
        except Exception as e:
            logger.error(f"❌ Ошибка запуска бота: {e}")
        
        time.sleep(30)

if __name__ == '__main__':
    logger.info("🚀 Сервер запускается...")
    
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌐 Flask запускается на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)