import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Импортируем функции клавиатур
from keyboards import get_main_keyboard, get_contacts_keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🤖 Бот Головина Романа - ЗАПУЩЕН")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"👤 Пользователь {user.first_name} начал чат")
    
    try:
        # Пробуем отправить фото
        if os.path.exists('assets/my_photo.png'):
            with open('assets/my_photo.png', 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption="👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь\n\nДобро пожаловать в мою визитную карточку!",
                    parse_mode='Markdown',
                    reply_markup=get_main_keyboard()
                )
        else:
            # Если фото нет, отправляем текст
            await update.message.reply_text(
                "👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь\n\nДобро пожаловать в мою визитную карточку!",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
    except Exception as e:
        print(f"❌ Ошибка при отправке фото: {e}")
        await update.message.reply_text(
            "👋 Привет! Я *Головин Роман*\n\n🏭 Старший контрольный мастер подземным\n💼 Ургалуголь",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"📨 Получено сообщение: {text}")
    
    # Обработка кнопок меню
    if text == "🔍 Обо мне":
        await update.message.reply_text(
            "🔍 **Обо мне:**\n\n"
            "С 2008 года развиваюсь вместе с предприятием \"Ургалуголь\", "
            "пройдя путь через ключевые подразделения: от внедрения SAP ERP "
            "и бухгалтерского контроля до управления клиентскими отношениями "
            "и технологического надзора.",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
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
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
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
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
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
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
    
    elif text == "🤖 Проекты ИИ":
        await update.message.reply_text(
            "🤖 **Проекты с ИИ:**\n\n"
            "*Текущие направления:*\n"
            "• Оптимизация рабочих задач сотрудников\n"
            "• Внедрение систем мониторинга процессов\n"
            "• Обработка и анализ видео\n"
            "• Разработка интеллектуальных систем контроля",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
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
    
    else:
        # Если сообщение не распознано, показываем меню
        await update.message.reply_text(
            "Выберите пункт из меню ниже:",
            reply_markup=get_main_keyboard()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на инлайн-кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "email":
        await query.edit_message_text("📧 Email: GolovinRV@suek.ru")
    elif query.data == "telegram":
        await query.edit_message_text("📱 Telegram: @CrazyRab1t\n💼 ID: 1290102754")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu - показывает главное меню"""
    await update.message.reply_text(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )

async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /contacts - показывает контакты"""
    await update.message.reply_text(
        "📞 **Контакты:**\n\n📧 Email: GolovinRV@suek.ru\n📱 Telegram: @CrazyRab1t",
        parse_mode='Markdown',
        reply_markup=get_contacts_keyboard()
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    print(f"❌ Ошибка: {context.error}")
    try:
        await update.message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")
    except:
        pass

def main():
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не найден!")
        return
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("contacts", contacts_command))
        
        # Добавляем обработчик инлайн-кнопок
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Добавляем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)
        
        print("✅ Бот инициализирован!")
        print("🤖 Запускаем polling...")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main()