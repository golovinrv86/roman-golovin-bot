import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Импортируем функции клавиатур
from keyboards import get_main_keyboard, get_contacts_keyboard, get_ai_consultant_keyboard

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 50)
print("🤖 БОТ ГОЛОВИНА РОМАНА - ЗАПУСК")
print("📸 Фото:", "✅ Найдено" if os.path.exists('assets/my_photo.png') else "❌ Не найдено")
print("=" * 50)

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"👤 Пользователь {user.first_name} начал чат")
    
    try:
        if os.path.exists('assets/my_photo.png'):
            with open('assets/my_photo.png', 'rb') as photo:
                update.message.reply_photo(
                    photo=photo,
                    caption="👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь\n\nДобро пожаловать в мою визитную карточку!",
                    parse_mode='Markdown',
                    reply_markup=get_main_keyboard()
                )
        else:
            update.message.reply_text(
                "👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        update.message.reply_text(
            "👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )

def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    responses = {
        "🔍 Обо мне": "🔍 **Обо мне:**\n\nС 2008 года развиваюсь вместе с предприятием \"Ургалуголь\", пройдя путь через ключевые подразделения...",
        "💼 Опыт работы": "💼 **Опыт работы:**\n\n*Ургалуголь* (02.2008 - настоящее время)\n\n• Старший контрольный мастер подземным\n• Ведущий специалист...",
        "🎓 Образование": "🎓 **Образование:**\n\n*Высшее образование:*\nАкадемия экономики и права\nСпециальность: Менеджмент на производстве...",
        "🛠 Навыки": "🛠 **Навыки:**\n\n*Профессиональные:*\n• Технологический контроль подземных работ\n• Внедрение SAP ERP...",
        "🤖 Проекты ИИ": "🤖 **Проекты с ИИ:**\n\n*Текущие направления:*\n• Оптимизация рабочих задач сотрудников\n• Внедрение систем мониторинга процессов...",
        "📞 Контакты": "📞 **Контакты:**\n\n📧 Email: GolovinRV@suek.ru\n📱 Telegram: @CrazyRab1t\n💼 ID: 1290102754"
    }
    
    if text in responses:
        update.message.reply_text(responses[text], parse_mode='Markdown', 
                                reply_markup=get_contacts_keyboard() if text == "📞 Контакты" else get_main_keyboard())
    elif text == "📰 Консультант ИИ":
        update.message.reply_text(
            "🤖 **Консультант ИИ**\n\nФункционал в разработке...",
            parse_mode='Markdown',
            reply_markup=get_ai_consultant_keyboard()
        )
    else:
        update.message.reply_text("Выберите пункт из меню ниже:", reply_markup=get_main_keyboard())

def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    
    if query.data == "email":
        query.edit_message_text("📧 Email: GolovinRV@suek.ru")
    elif query.data == "telegram":
        query.edit_message_text("📱 Telegram: @CrazyRab1t\n💼 ID: 1290102754")

def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text("Главное меню:", reply_markup=get_main_keyboard())

def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text(
        "📞 **Контакты:**\n\n📧 Email: GolovinRV@suek.ru\n📱 Telegram: @CrazyRab1t",
        parse_mode='Markdown',
        reply_markup=get_contacts_keyboard()
    )

def main():
    """Основная функция для запуска бота"""
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        return
    
    print("✅ Бот инициализируется...")
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("contacts", contacts_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ Бот запускает polling...")
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка бота: {e}")

if __name__ == "__main__":
    main()