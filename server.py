from flask import Flask
import os
import threading
import asyncio
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот Головина Романа работает! Telegram: @UCHEBAutk_bot"

@app.route('/health')
def health():
    return "OK"

def run_bot():
    """Запускает бота в отдельном потоке"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        from bot import main
        loop.run_until_complete(main())
    except Exception as e:
        logging.exception("Ошибка в боте")
    finally:
        loop.close()

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("✅ Бот запущен в отдельном потоке")

    # Запускаем Flask сервер
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)