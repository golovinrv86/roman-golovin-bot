from flask import Flask
import os
import subprocess
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот Головина Романа работает! Telegram: @UCHEBAutk_bot"

@app.route('/health')
def health():
    return "OK"

@app.route('/yandex-status')
def yandex_status():
    try:
        from yandex_gpt import yandex_gpt
        status = "настроен" if yandex_gpt.is_configured() else "не настроен"
        return f"Yandex GPT: {status}"
    except Exception as e:
        return f"Error: {e}"

def run_bot():
    """Запускает бота в отдельном процессе"""
    time.sleep(10)
    while True:
        try:
            print("🔄 Запускаем бота...")
            # Пробуем python3
            process = subprocess.run(['python3', 'bot.py'], 
                                   capture_output=True, 
                                   text=True,
                                   timeout=30)
            print("Вывод бота:", process.stdout)
            if process.stderr:
                print("Ошибки бота:", process.stderr)
        except subprocess.TimeoutExpired:
            print("⏰ Бот работает... перезапускаем")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        
        time.sleep(10)

if __name__ == '__main__':
    print("🚀 Сервер запускается...")
    
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)