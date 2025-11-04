from flask import Flask
import os
import subprocess
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот Головина Романа работает! Telegram: @UCHEBAutk_bot"

@app.route('/health')
def health():
    return "OK"

def run_bot():
    """Запускает бота в отдельном процессе"""
    try:
        subprocess.run([sys.executable, "bot.py"], check=True)
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    import sys
    
    # Запускаем бота в отдельном процессе
    bot_process = threading.Thread(target=run_bot, daemon=True)
    bot_process.start()
    print("✅ Бот запущен в отдельном процессе")
    
    # Запускаем Flask сервер
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)