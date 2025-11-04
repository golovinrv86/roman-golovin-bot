from flask import Flask
import os
import subprocess
import threading
import time
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот Головина Романа работает! Telegram: @UCHEBAutk_bot"

@app.route('/health')
def health():
    return "OK"

@app.route('/bot-status')
def bot_status():
    return "Бот запущен и работает!"

def run_bot():
    """Запускает бота в отдельном процессе с перезапуском при падении"""
    while True:
        try:
            print("🔄 ЗАПУСКАЕМ БОТА...")
            # Запускаем бота как subprocess
            process = subprocess.Popen([sys.executable, 'bot.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True)
            
            # Читаем вывод в реальном времени
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(f"🤖 БОТ: {output.strip()}")
            
            # Если процесс завершился
            return_code = process.poll()
            if return_code == 0:
                print("✅ Бот завершил работу нормально")
                break
            else:
                print(f"🔄 Бот упал с кодом {return_code}, перезапускаем...")
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ Ошибка запуска бота: {e}")
            time.sleep(10)

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 ЗАПУСК СЕРВЕРА И БОТА")
    print("=" * 50)
    
    # Проверяем переменные окружения
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    else:
        print("✅ BOT_TOKEN: найден")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("✅ Бот запущен в фоновом режиме")
    
    # Запускаем Flask сервер
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Flask сервер запускается на порту {port}")
    print(f"📡 URL: http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)