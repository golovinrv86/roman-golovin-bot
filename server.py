from flask import Flask
import os
import subprocess
import threading
import time
import sys
import shutil

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот Головина Романа работает! Telegram: @UCHEBAutk_bot"

@app.route('/health')
def health():
    return "OK"

def find_python_command():
    """Находит правильную команду для запуска Python"""
    # Проверяем доступные команды Python
    for cmd in ['python3', 'python', 'py']:
        if shutil.which(cmd):
            print(f"✅ Найдена команда Python: {cmd}")
            return cmd
    print("❌ Не найдена команда Python!")
    return 'python'  # fallback

def run_bot():
    """Запускает бота в отдельном процессе"""
    python_cmd = find_python_command()
    print(f"🔄 Используем команду: {python_cmd}")
    
    time.sleep(5)
    
    while True:
        try:
            print("🔄 ЗАПУСКАЕМ БОТА...")
            print(f"📁 Текущая директория: {os.getcwd()}")
            print(f"📁 Существует ли bot.py: {os.path.exists('bot.py')}")
            
            # Запускаем бота с правильной командой Python
            process = subprocess.Popen([python_cmd, 'bot.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT,
                                     text=True,
                                     bufsize=1,
                                     universal_newlines=True)
            
            print(f"✅ Процесс бота запущен с PID: {process.pid}")
            
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