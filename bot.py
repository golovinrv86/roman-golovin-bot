import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Импортируем модули
from keyboards import get_main_keyboard, get_contacts_keyboard, get_ai_consultant_keyboard, get_consultant_active_keyboard
from yandex_gpt import yandex_gpt
from session_manager import session_manager

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🤖 Бот Головина Романа - ЗАПУЩЕН")
print(f"✅ Yandex GPT: {'настроен' if yandex_gpt.is_configured() else 'не настроен'}")
if yandex_gpt.is_configured():
    print(f"🔧 Folder ID: {yandex_gpt.folder_id}")
    print(f"🔧 API Key: {'установлен' if yandex_gpt.api_key else 'отсутствует'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"👤 Пользователь {user.first_name} начал чат")
    
    # Очищаем сессию пользователя
    session_manager.clear_consultant_topic(user.id)
    
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

async def handle_consultant_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question: str):
    """Обрабатывает вопросы для AI-консультанта"""
    user_id = update.message.from_user.id
    
    print(f"🤖 Вопрос консультанту от {user_id}: {question}")
    
    # Проверяем, есть ли активная сессия консультанта
    if not session_manager.is_in_consultant_mode(user_id):
        await update.message.reply_text(
            "❌ Сначала выберите тему для консультации.",
            reply_markup=get_ai_consultant_keyboard()
        )
        return
    
    topic = session_manager.get_consultant_topic(user_id)
    
    # Показываем, что бот "печатает"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Отправляем вопрос в Yandex GPT
        answer = await yandex_gpt.ask_question(question, topic)
        
        # Отправляем ответ пользователю
        await update.message.reply_text(
            f"🤖 *Ответ консультанта ({topic.replace('_', ' ').title()}):*\n\n{answer}",
            parse_mode='Markdown',
            reply_markup=get_consultant_active_keyboard()
        )
        
    except Exception as e:
        print(f"❌ Ошибка при обработке вопроса: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обращении к AI-консультанту. Попробуйте еще раз.",
            reply_markup=get_consultant_active_keyboard()
        )

async def handle_consultant_topic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, topic_key: str, topic_name: str, description: str):
    """Обрабатывает выбор темы консультанта"""
    user_id = update.message.from_user.id
    
    # Устанавливаем тему
    session_manager.set_consultant_topic(user_id, topic_key)
    
    print(f"🎯 Пользователь {user_id} выбрал тему: {topic_name}")
    
    await update.message.reply_text(
        f"{topic_name}\n\n"
        f"{description}\n\n"
        "✅ *Тема установлена!*\n\n"
        "Теперь просто напишите ваш вопрос в чат, и я передам его AI-консультанту.\n\n"
        "Для возврата к выбору темы нажмите '🔙 Назад к темам'",
        parse_mode='Markdown',
        reply_markup=get_consultant_active_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    print(f"📨 Получено сообщение от {user_id}: '{text}'")
    
    # ПЕРВОЕ: если пользователь в режиме консультанта и это не команда навигации - обрабатываем как вопрос
    if (session_manager.is_in_consultant_mode(user_id) and 
        text not in ["🔙 Назад к темам", "📋 Главное меню", "📰 Консультант ИИ"]):
        await handle_consultant_question(update, context, text)
        return
    
    # ВТОРОЕ: обработка навигационных команд
    if text == "🔍 Обо мне":
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "🔍 **Обо мне:**\n\n"
            "С 2008 года развиваюсь вместе с предприятием \"Ургалуголь\", "
            "пройдя путь через ключевые подразделения: от внедрения SAP ERP "
            "и бухгалтерского контроля до управления клиентскими отношениями "
            "и технологического надзора.\n\n"
            "*Ключевые достижения:*\n"
            "• Внедрение систем контроля качества\n"
            "• Оптимизация производственных процессов\n"
            "• Разработка и внедрение AI-решений\n"
            "• Повышение эффективности работы отделов",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    elif text == "💼 Опыт работы":
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "💼 **Опыт работы:**\n\n"
            "*Ургалуголь* (02.2008 - настоящее время)\n\n"
            "• *Старший контрольный мастер подземным* - контроль качества работ, оптимизация процессов\n"
            "• *Ведущий специалист - Погрузочно-транспортный участок* - управление логистикой\n"
            "• *Менеджер по работе с клиентами* - развитие клиентской базы\n"
            "• *Специалист отдела учета услуг* - аналитика и отчетность\n"
            "• *Специалист по внедрению ПО SAP ERP* - цифровизация процессов\n\n"
            "*Общий стаж:* 16+ лет\n"
            "*Отрасль:* Угольная промышленность",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    elif text == "🎓 Образование":
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "🎓 **Образование:**\n\n"
            "*Высшее образование:*\n"
            "🎓 Академия экономики и права\n"
            "📚 Специальность: Менеджмент на производстве\n"
            "📅 Год окончания: 2015\n\n"
            "*Среднее специальное образование:*\n"
            "🎓 Хабаровская Банковская Школа\n"
            "📚 Специальность: Специалист банковского дела\n"
            "📅 Год окончания: 2008\n\n"
            "*Дополнительное образование:*\n"
            "• Курсы по искусственному интеллекту\n"
            "• Программы повышения квалификации в угольной отрасли",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    elif text == "🛠 Навыки":
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "🛠 **Навыки:**\n\n"
            "*Профессиональные:*\n"
            "• Технологический контроль подземных работ\n"
            "• Внедрение SAP ERP и цифровых систем\n"
            "• Управление качеством угля\n"
            "• Работа с клиентами и партнерами\n"
            "• Бухгалтерский контроль и отчетность\n"
            "• Оптимизация производственных процессов\n\n"
            "*Технические:*\n"
            "• Уверенный пользователь MS Office\n"
            "• Опыт работы с Python и AI-библиотеками\n"
            "• Работа с искусственным интеллектом\n"
            "• Анализ данных и аналитика\n"
            "• Системы мониторинга и контроля",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    elif text == "🤖 Проекты ИИ":
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "🤖 **Проекты с ИИ:**\n\n"
            "*Текущие направления:*\n"
            "• Оптимизация рабочих задач сотрудников с помощью AI\n"
            "• Внедрение систем мониторинга процессов в реальном времени\n"
            "• Обработка и анализ видео для контроля качества\n"
            "• Разработка интеллектуальных систем контроля производства\n"
            "• Predictive maintenance - прогнозное обслуживание оборудования\n\n"
            "*Достижения:*\n"
            "• Повышение эффективности контроля на 30%\n"
            "• Снижение времени обработки данных на 50%\n"
            "• Автоматизация рутинных операций",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    elif text == "📞 Контакты":
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "📞 **Контакты:**\n\n"
            "📧 *Email:* GolovinRV@suek.ru\n"
            "📱 *Telegram:* @CrazyRab1t\n"
            "💼 *ID:* 1290102754\n\n"
            "*Рабочие контакты:*\n"
            "🏭 Компания: Ургалуголь\n"
            "📍 Место работы: Чегдомын, Хабаровский край",
            parse_mode='Markdown',
            reply_markup=get_contacts_keyboard()
        )
        return
    
    elif text == "📰 Консультант ИИ":
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "🤖 **Консультант ИИ**\n\n"
            "Выберите тему для консультации:\n\n"
            "🏭 *Угольная промышленность* - технологии добычи, оборудование, безопасность, процессы\n"
            "📊 *Качество угля* - стандарты, методики, контроль качества, параметры\n"
            "🚀 *Искусственный интеллект* - внедрение ИИ в производство, оптимизация\n\n"
            "После выбора темы просто напишите ваш вопрос в чат, и AI-консультант даст профессиональный ответ.",
            parse_mode='Markdown',
            reply_markup=get_ai_consultant_keyboard()
        )
        return
    
    # Обработка тем консультанта
    elif text == "🏭 Угольная промышленность":
        await handle_consultant_topic_selection(
            update, context,
            "угольная_промышленность",
            "🏭 *Консультант по угольной промышленности*",
            "Задавайте вопросы по:\n"
            "• Технологиям добычи угля\n"
            "• Оборудованию и технике\n"  
            "• Технике безопасности\n"
            "• Процессам обогащения\n"
            "• Логистике и транспортировке\n"
            "• Производственным процессам\n"
            "• Нормативам и стандартам"
        )
        return
    
    elif text == "📊 Качество угля":
        await handle_consultant_topic_selection(
            update, context,
            "качество_угля", 
            "📊 *Консультант по качеству угля*",
            "Задавайте вопросы по:\n"
            "• Методам оценки качества\n"
            "• Параметрам качества (зольность, влажность)\n"
            "• Стандартам и нормативам\n"
            "• Лабораторным исследованиям\n"
            "• Сертификации продукции\n"
            "• Контролю на всех этапах\n"
            "• Маркировке и классификации"
        )
        return
    
    elif text == "🚀 Искусственный интеллект":
        await handle_consultant_topic_selection(
            update, context,
            "искусственный_интеллект",
            "🚀 *Консультант по искусственному интеллекту*",
            "Задавайте вопросы по:\n"
            "• Внедрению ИИ в производство\n"
            "• Компьютерному зрению\n"
            "• Predictive maintenance\n"
            "• Анализу данных\n"
            "• Оптимизации процессов\n"
            "• Автоматизации операций\n"
            "• Цифровой трансформации"
        )
        return
    
    elif text == "🔙 Назад к темам":
        # Возвращаем к выбору тем консультанта
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "🤖 **Выберите тему для консультации:**\n\n"
            "Я готов ответить на ваши вопросы по выбранному направлению:",
            parse_mode='Markdown',
            reply_markup=get_ai_consultant_keyboard()
        )
        return
    
    elif text == "📋 Главное меню":
        # Возвращаем в главное меню
        session_manager.clear_consultant_topic(user_id)
        await update.message.reply_text(
            "🏠 *Главное меню*\n\n"
            "Выберите интересующий вас раздел:",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        return
    
    else:
        # Если сообщение не распознано
        if session_manager.is_in_consultant_mode(user_id):
            await update.message.reply_text(
                "🤖 *Вы в режиме консультанта*\n\n"
                "Просто напишите ваш вопрос в чат, и я передам его AI-консультанту.\n\n"
                "Для возврата к выбору темы нажмите '🔙 Назад к темам'\n"
                "Для выхода в главное меню нажмите '📋 Главное меню'",
                parse_mode='Markdown',
                reply_markup=get_consultant_active_keyboard()
            )
        else:
            # Если нет активной темы - показываем меню
            await update.message.reply_text(
                "🤖 *Визитная карточка Головина Романа*\n\n"
                "Выберите пункт из меню ниже:",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на инлайн-кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "email":
        await query.edit_message_text(
            "📧 *Email для связи:*\n\n"
            "GolovinRV@suek.ru\n\n"
            "Рабочая почта для деловых предложений и вопросов.",
            parse_mode='Markdown'
        )
    elif query.data == "telegram":
        await query.edit_message_text(
            "📱 *Telegram контакты:*\n\n"
            "👤 @CrazyRab1t\n"
            "💼 ID: 1290102754\n\n"
            "Предпочтительный способ для оперативной связи.",
            parse_mode='Markdown'
        )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu - показывает главное меню"""
    user_id = update.message.from_user.id
    session_manager.clear_consultant_topic(user_id)
    await update.message.reply_text(
        "🏠 *Главное меню*\n\n"
        "Выберите интересующий вас раздел:",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /contacts - показывает контакты"""
    await update.message.reply_text(
        "📞 **Контакты:**\n\n"
        "📧 *Email:* GolovinRV@suek.ru\n"
        "📱 *Telegram:* @CrazyRab1t\n"
        "💼 *ID:* 1290102754\n\n"
        "Для быстрой связи используйте кнопки ниже:",
        parse_mode='Markdown',
        reply_markup=get_contacts_keyboard()
    )

async def consultant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /consultant - запускает AI-консультанта"""
    user_id = update.message.from_user.id
    session_manager.clear_consultant_topic(user_id)
    await update.message.reply_text(
        "🤖 **Консультант ИИ**\n\n"
        "Выберите тему для консультации:",
        parse_mode='Markdown',
        reply_markup=get_ai_consultant_keyboard()
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    print(f"❌ Ошибка: {context.error}")
    try:
        await update.message.reply_text(
            "❌ Произошла ошибка. Попробуйте еще раз или вернитесь в главное меню командой /menu",
            reply_markup=get_main_keyboard()
        )
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
        application.add_handler(CommandHandler("consultant", consultant_command))
        
        # Добавляем обработчик инлайн-кнопок
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Добавляем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)
        
        print("✅ Бот инициализирован с реальным Yandex GPT!")
        print("🤖 Запускаем polling...")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

if __name__ == "__main__":
    main()