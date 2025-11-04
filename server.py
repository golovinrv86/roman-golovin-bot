from flask import Flask
import os
import asyncio
import threading
import logging

app = Flask(__name__)

# Глобальная переменная для хранения задачи бота
bot_task = None

@app.route('/')
def home():
    return "🤖 Бот Головина Романа работает! Telegram: @UCHEBAutk_bot"

@app.route('/health')
def health():
    return "OK"

def run_async_task():
    """Запускает асинхронную задачу в отдельном event loop"""
    global bot_task
    
    try:
        # Создаем новый event loop для этого потока
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Импортируем и запускаем бота
        from bot import main
        
        # Запускаем бота
        bot_task = asyncio.ensure_future(main(), loop=loop)
        loop.run_until_complete(bot_task)
        
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if bot_task and not bot_task.done():
            bot_task.cancel()

if __name__ == '__main__':
    print("🚀 Запуск приложения...")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_async_task, daemon=True)
    bot_thread.start()
    print("✅ Бот запущен в отдельном потоке")
    
    # Запускаем Flask сервер в основном потоке
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Запуск Flask сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)