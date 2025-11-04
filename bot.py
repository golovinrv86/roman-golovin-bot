import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Импортируем функции клавиатур
from keyboards import get_main_keyboard, get_contacts_keyboard, get_ai_consultant_keyboard, get_back_to_consultant_keyboard
from yandex_gpt import yandex_gpt  # Импортируем Yandex GPT

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🤖 Бот Головина Романа - ЗАПУЩЕН")
print(f"✅ Yandex GPT: {'настроен' if yandex_gpt.is_configured() else 'не настроен'}")

# Глобальная переменная для хранения текущей темы консультации
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"👤 Пользователь {user.first_name} начал чат")
    
    # Очищаем сессию пользователя
    user_sessions[user.id] = {"consultant_topic": None}
    
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
    user_id = update.message.from_user.id
    text = update.message.text
    print(f"📨 Получено сообщение от {user_id}: {text}")
    
    # Проверяем, находится ли пользователь в режиме консультанта
    if user_id in user_sessions and user_sessions[user_id].get("consultant_topic"):
        await handle_consultant_question(update, context)
        return
    
    # Обработка кнопок меню
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
            "Выберите тему для консультации:\n\n"
            "🏭 *Угольная промышленность* - технологии добычи, оборудование, безопасность\n"
            "📊 *Качество угля* - стандарты, методики, контроль качества\n"
            "🚀 *Искусственный интеллект* - внедрение ИИ в производство\n\n"
            "После выбора темы вы можете задавать вопросы AI-консультанту.",
            parse_mode='Markdown',
            reply_markup=get_ai_consultant_keyboard()
        )
    
    # Обработка тем консультанта
    elif text == "🏭 Угольная промышленность":
        user_sessions[user_id] = {"consultant_topic": "угольная_промышленность"}
        await update.message.reply_text(
            "🏭 *Консультант по угольной промышленности*\n\n"
            "Задавайте вопросы по:\n"
            "• Технологиям добычи угля\n"
            "• Оборудованию и технике\n"  
            "• Технике безопасности\n"
            "• Процессам обогащения\n"
            "• Логистике и транспортировке\n\n"
            "Для возврата к выбору темы нажмите 'Назад к темам'",
            parse_mode='Markdown',
            reply_markup=get_back_to_consultant_keyboard()
        )
    
    elif text == "📊 Качество угля":
        user_sessions[user_id] = {"consultant_topic": "качество_угля"}
        await update.message.reply_text(
            "📊 *Консультант по качеству угля*\n\n"
            "Задавайте вопросы по:\n"
            "• Методам оценки качества\n"
            "• Параметрам качества (зольность, влажность)\n"
            "• Стандартам и нормативам\n"
            "• Лабораторным исследованиям\n"
            "• Сертификации продукции\n\n"
            "Для возврата к выбору темы нажмите 'Назад к темам'",
            parse_mode='Markdown',
            reply_markup=get_back_to_consultant_keyboard()
        )
    
    elif text == "🚀 Искусственный интеллект":
        user_sessions[user_id] = {"consultant_topic": "искусственный_интеллект"}
        await update.message.reply_text(
            "🚀 *Консультант по искусственному интеллекту*\n\n"
            "Задавайте вопросы по:\n"
            "• Внедрению ИИ в производство\n"
            "• Компьютерному зрению\n"
            "• Predictive maintenance\n"
            "• Анализу данных\n"
            "• Оптимизации процессов\n\n"
            "Для возврата к выбору темы нажмите 'Назад к темам'",
            parse_mode='Markdown',
            reply_markup=get_back_to_consultant_keyboard()
        )
    
    elif text == "🔙 Назад к темам" or text == "📋 Главное меню":
        # Возвращаем в главное меню
        if user_id in user_sessions:
            user_sessions[user_id]["consultant_topic"] = None
        
        if text == "🔙 Назад к темам":
            await update.message.reply_text(
                "Выберите тему для консультации:",
                reply_markup=get_ai_consultant_keyboard()
            )
        else:
            await update.message.reply_text(
                "Главное меню:",
                reply_markup=get_main_keyboard()
            )
    
    else:
        await update.message.reply_text(
            "Выберите пункт из меню ниже:",
            reply_markup=get_main_keyboard()
        )

async def handle_consultant_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает вопросы для AI-консультанта"""
    user_id = update.message.from_user.id
    question = update.message.text
    
    # Показываем, что бот "печатает"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    topic = user_sessions[user_id]["consultant_topic"]
    
    # Отправляем вопрос в Yandex GPT
    answer = await yandex_gpt.ask_question(question, topic)
    
    # Отправляем ответ пользователю
    await update.message.reply_text(
        f"🤖 *Ответ консультанта:*\n\n{answer}",
        parse_mode='Markdown',
        reply_markup=get_back_to_consultant_keyboard()
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
    user_id = update.message.from_user.id
    # Очищаем сессию консультанта
    if user_id in user_sessions:
        user_sessions[user_id]["consultant_topic"] = None
    
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
        
        print("✅ Бот инициализирован с полной логикой!")
        print("🤖 Запускаем polling...")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main()