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

def run_bot():
    """Запускает бота в отдельном процессе с улучшенным логированием"""
    print("🔄 Функция run_bot() запущена")
    time.sleep(5)  # Уменьшили задержку до 5 секунд
    print("🔄 Задержка завершена, запускаем бота...")
    
    while True:
        try:
            print("🔄 ЗАПУСКАЕМ БОТА...")
            print(f"📁 Текущая директория: {os.getcwd()}")
            print(f"📁 Существует ли bot.py: {os.path.exists('bot.py')}")
            
            # Запускаем бота как subprocess с выводом в реальном времени
            process = subprocess.Popen([sys.executable, 'bot.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT,
                                     text=True,
                                     bufsize=1,
                                     universal_newlines=True)
            
            print("✅ Процесс бота запущен, PID:", process.pid)
            
            # Читаем вывод в реальном времени
            for line in iter(process.stdout.readline, ''):
                if line:
                    print(f"🤖 БОТ: {line.strip()}")
            
            # Ждем завершения процесса
            process.wait()
            return_code = process.returncode
            
            print(f"🔴 Бот завершил работу с кодом: {return_code}")
            
            if return_code == 0:
                print("✅ Бот завершил работу нормально")
                break
            else:
                print(f"🔄 Бот упал, перезапускаем через 10 секунд...")
                time.sleep(10)
                
        except Exception as e:
            print(f"❌ Ошибка запуска бота: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(10)

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 ЗАПУСК СЕРВЕРА И БОТА")
    print("=" * 50)
    
    # Проверяем переменные окружения
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    print(f"✅ BOT_TOKEN: {'найден' if BOT_TOKEN else 'НЕ НАЙДЕН'}")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("✅ Поток бота запущен")
    
    # Запускаем Flask сервер
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Flask сервер запускается на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)