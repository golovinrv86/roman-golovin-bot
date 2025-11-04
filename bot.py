async def main():
    """Основная асинхронная функция для запуска бота"""
    
    # Получаем все переменные окружения
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    YANDEX_API_KEY = os.environ.get('YANDEX_GPT_API_KEY')
    YANDEX_FOLDER_ID = os.environ.get('YANDEX_FOLDER_ID')

    # Проверка переменных
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        return
    
    if not YANDEX_API_KEY:
        print("⚠️  Предупреждение: YANDEX_GPT_API_KEY не найден")
    
    if not YANDEX_FOLDER_ID:
        print("⚠️  Предупреждение: YANDEX_FOLDER_ID не найден")
    
    print("✅ Все переменные окружения загружены успешно!")

    try:
        # Создаем приложение бота
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("contacts", contacts_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ Бот успешно инициализирован!")
        print("🤖 Запускаем polling...")
        
        # Запускаем бота
        await application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        import traceback
        traceback.print_exc()