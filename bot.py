import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Импортируем функции клавиатур
from keyboards import get_main_keyboard, get_contacts_keyboard, get_ai_consultant_keyboard

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("=" * 50)
print("🤖 БОТ ГОЛОВИНА РОМАНА - РАБОЧАЯ ВЕРСИЯ")
print("✅ Клавиатуры загружены")
print("📸 Фото: ✅ Найдено" if os.path.exists('assets/my_photo.png') else "❌ Не найдено")
print("=" * 50)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"👤 Пользователь {user.first_name} начал чат")
    
    try:
        if os.path.exists('assets/my_photo.png'):
            with open('assets/my_photo.png', 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption="👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь\n\nДобро пожаловать в мою визитную карточку!",
                    parse_mode='Markdown',
                    reply_markup=get_main_keyboard()
                )
        else:
            await update.message.reply_text(
                "👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await update.message.reply_text(
            "👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🔍 Обо мне":
        await update.message.reply_text(
            "🔍 **Обо мне:**\n\n"
            "С 2008 года развиваюсь вместе с предприятием \"Ургалуголь\", "
            "пройдя путь через ключевые подразделения: от внедрения SAP ERP "
            "и бухгалтерского контроля до управления клиентскими отношениями "
            "и технологического надзора.",
            parse_mode='Markdown'
        )
    
    elif text == "💼 Опыт работы":
        await update.message.reply_text(
            "💼 **Опыт работы:**\n\n"
            "*Ургалуголь* (02.2008 - настоящее время)\n\n"
            "• Старший контрольный мастер подземным\n"
            "• Ведущий специалист - Погрузочно-транспортный участок\n"
            "• Менеджер по работе с клиентами\n"
            "• Специалист отдела учета услуг\n"
            "• Специалист по внедрению ПО SAP ERP\n\n"
            "*Общий стаж:* 16+ лет",
            parse_mode='Markdown'
        )
    
    elif text == "🎓 Образование":
        await update.message.reply_text(
            "🎓 **Образование:**\n\n"
            "*Высшее образование:*\n"
            "Академия экономики и права\n"
            "Специальность: Менеджмент на производстве\n\n"
            "*Среднее специальное образование:*\n"
            "Хабаровская Банковская Школа\n"
            "Специальность: Специалист банковского дела",
            parse_mode='Markdown'
        )
    
    elif text == "🛠 Навыки":
        await update.message.reply_text(
            "🛠 **Навыки:**\n\n"
            "*Профессиональные:*\n"
            "• Технологический контроль подземных работ\n"
            "• Внедрение SAP ERP\n"
            "• Работа с клиентами\n"
            "• Бухгалтерский контроль\n\n"
            "*Технические:*\n"
            "• Уверенный пользователь MS Office\n"
            "• Опыт работы с Python\n"
            "• Работа с искусственным интеллектом",
            parse_mode='Markdown'
        )
    
    elif text == "🤖 Проекты ИИ":
        await update.message.reply_text(
            "🤖 **Проекты с ИИ:**\n\n"
            "*Текущие направления:*\n"
            "• Оптимизация рабочих задач сотрудников\n"
            "• Внедрение систем мониторинга процессов\n"
            "• Обработка и анализ видео\n"
            "• Разработка интеллектуальных систем контроля",
            parse_mode='Markdown'
        )
    
    elif text == "📞 Контакты":
        await update.message.reply_text(
            "📞 **Контакты:**\n\n"
            "📧 Email: GolovinRV@suek.ru\n"
            "📱 Telegram: @CrazyRab1t\n"
            "💼 ID: 1290102754",
            parse_mode='Markdown',
            reply_markup=get_contacts_keyboard()
        )
    
    elif text == "📰 Консультант ИИ":
        await update.message.reply_text(
            "🤖 **Консультант ИИ**\n\n"
            "В этом разделе вы можете задать вопросы по темам:\n\n"
            "🏭 Угольная промышленность\n"
            "📊 Качество угля\n"
            "🚀 Искусственный интеллект\n\n"
            "Функционал в разработке...",
            parse_mode='Markdown',
            reply_markup=get_ai_consultant_keyboard()
        )
    
    else:
        await update.message.reply_text(
            "Выберите пункт из меню ниже:",
            reply_markup=get_main_keyboard()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "email":
        await query.edit_message_text("📧 Email: GolovinRV@suek.ru")
    elif query.data == "telegram":
        await query.edit_message_text("📱 Telegram: @CrazyRab1t\n💼 ID: 1290102754")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )

async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 **Контакты:**\n\n📧 Email: GolovinRV@suek.ru\n📱 Telegram: @CrazyRab1t",
        parse_mode='Markdown',
        reply_markup=get_contacts_keyboard()
    )

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

# Старая синхронная функция main для обратной совместимости
def sync_main():
    """Синхронная версия для запуска бота отдельно"""
    asyncio.run(main())

if __name__ == "__main__":
    sync_main()