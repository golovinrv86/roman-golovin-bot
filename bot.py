import os
import logging
import sys
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

print("=" * 60)
print("🤖 Бот Головина Романа запускается...")
print("📁 Текущая директория:", os.getcwd())

# Проверка переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
print("🔑 BOT_TOKEN:", "✅ Установлен" if BOT_TOKEN else "❌ Отсутствует")

if BOT_TOKEN:
    print("🔑 Длина токена:", len(BOT_TOKEN))

print("=" * 60)

# Проверка папки assets
if os.path.exists('assets'):
    print("📸 Папка assets найдена")
    if os.path.exists('assets/my_photo.png'):
        print("✅ Фото my_photo.png найдено")
    else:
        print("❌ Фото my_photo.png не найдено")
else:
    print("❌ Папка assets не найдена")

# Импорты после диагностики
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

# Хранилище для ограничения запросов
user_requests = {}
user_questions = {}

async def set_bot_commands(application: Application):
    """Устанавливаем команды бота"""
    commands = [
        ("start", "Запустить бота"),
        ("menu", "Показать главное меню"),
        ("contacts", "Показать контакты")
    ]
    await application.bot.set_my_commands(commands)

def can_make_request(user_id):
    """Проверяет, может ли пользователь сделать запрос"""
    now = datetime.now()
    
    # Админ имеет неограниченный доступ
    if user_id == 1290102754:
        return True, "OK"
    
    if user_id not in user_requests:
        user_requests[user_id] = []
    
    # Удаляем старые запросы (старше 24 часов)
    user_requests[user_id] = [req_time for req_time in user_requests[user_id] 
                             if now - req_time < timedelta(days=1)]
    
    # Проверяем лимит
    if len(user_requests[user_id]) >= 3:
        remaining_time = timedelta(days=1) - (now - min(user_requests[user_id]))
        hours = int(remaining_time.total_seconds() // 3600)
        minutes = int((remaining_time.total_seconds() % 3600) // 60)
        return False, f"Лимит запросов исчерпан. Попробуйте через {hours}ч {minutes}м"
    
    return True, "OK"

def record_request(user_id):
    """Записывает время запроса пользователя"""
    if user_id not in user_requests:
        user_requests[user_id] = []
    user_requests[user_id].append(datetime.now())

def is_topic_allowed(question):
    """Проверяет, соответствует ли вопрос разрешенным темам"""
    question_lower = question.lower()
    allowed_keywords = [
        "ургалуголь", "суэк", "уголь", "добыча", "обогащение", "отгрузка", 
        "производство", "качество угля", "зольность", "влажность", "калорийность",
        "угольная промышленность", "зарождение", "история", "развитие",
        "технология", "обогатительная", "карьер", "шахта", "марка угля",
        "теплота сгорания", "сера", "летучие", "кокс", "энергетический",
        "ии", "искусственный интеллект", "ai", "машинное обучение", 
        "нейросеть", "компьютерное зрение", "обработка данных"
    ]
    
    return any(keyword in question_lower for keyword in allowed_keywords)

def ask_yandex_gpt(question, user_id):
    """Запрос к Yandex GPT"""
    can_request, message = can_make_request(user_id)
    if not can_request:
        return message
    
    if not is_topic_allowed(question):
        return ("❌ **Тематика ограничена!**\n\n"
               "Я могу отвечать только на вопросы по темам:\n\n"
               "🏭 **Угольная промышленность:**\n"
               "• Качество угля и параметры\n"
               "• Ургалуголь и СУЭК\n"
               "• Технологии добычи и обогащения\n\n"
               "🤖 **Искусственный интеллект:**\n"
               "• Новости и тренды ИИ\n"
               "• Достижения и успехи\n\n"
               "Пожалуйста, задайте вопрос в рамках этих тем.")
    
    try:
        record_request(user_id)
        
        # Демо-ответы
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["зольность", "влага", "калорийность"]):
            demo_responses = [
                "🏭 **Эксперт по качеству угля:**\n\nЗольность, влажность и калорийность - ключевые параметры качества угля. Повышенная зольность снижает теплоту сгорания, а высокая влажность требует дополнительных затрат на сушку.",
                "🏭 **Эксперт по качеству угля:**\n\nКалорийность угля обратно пропорциональна зольности и влажности. При зольности выше 25% значительно падает энергетическая ценность."
            ]
        elif any(word in question_lower for word in ["ии", "искусственный интеллект"]):
            demo_responses = [
                "🤖 **Эксперт по ИИ:**\n\nВ 2024 году ИИ достиг значительных успехов: мультимодальные модели, улучшенная обработка естественного языка, применение в медицине и промышленности.",
                "🤖 **Эксперт по ИИ:**\n\nКлючевые достижения ИИ: генеративный AI создает качественный контент, компьютерное зрение точно идентифицирует объекты."
            ]
        else:
            demo_responses = [
                "🏭 **Эксперт по угольной промышленности:**\n\nУгольная промышленность России активно развивается, внедряя современные технологии добычи и обогащения.",
                "🤖 **Консультант по технологиям:**\n\nСовременные технологии позволяют значительно повысить эффективность угледобычи."
            ]
        
        import random
        return random.choice(demo_responses)
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return "⚠️ Сервис временно недоступен. Попробуйте позже."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} начал разговор")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    photo_path = os.path.join(current_dir, "assets/my_photo.png")
    
    if os.path.exists(photo_path):
        try:
            with open(photo_path, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=f"👋 Привет, {user.first_name}!\n\nМеня зовут *Головин Роман*\nСтарший контрольный мастер подземным\nУргалуголь\n\nДобро пожаловать в мою визитную карточку!",
                    parse_mode='Markdown',
                    reply_markup=get_main_keyboard()
                )
        except Exception as e:
            await send_text_message(update)
    else:
        await send_text_message(update)

async def send_text_message(update: Update):
    await update.message.reply_text(
        f"👋 Привет!\n\nМеня зовут *Головин Роман*\nСтарший контрольный мастер подземным\nУргалуголь\n\nДобро пожаловать в мою визитную карточку!",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.message.from_user.id
    
    if user_id in user_questions and user_questions[user_id]:
        question = text
        del user_questions[user_id]
        
        await update.message.reply_text("🔄 Консультирую...")
        answer = ask_yandex_gpt(question, user_id)
        await update.message.reply_text(answer, parse_mode='Markdown')
        return
    
    if text == "🔍 Обо мне":
        await update.message.reply_text("🔍 **Обо мне:**\n\nС 2008 года развиваюсь вместе с предприятием \"Ургалуголь\", пройдя путь через ключевые подразделения: от внедрения SAP ERP и бухгалтерского контроля до управления клиентскими отношениями и технологического надзора.", parse_mode='Markdown')
    
    elif text == "💼 Опыт работы":
        await update.message.reply_text("💼 **Опыт работы:**\n\n*Ургалуголь* (02.2008 - настоящее время)\n\n• Старший контрольный мастер подземным\n• Ведущий специалист - Погрузочно-транспортный участок\n• Менеджер по работе с клиентами\n• Специалист отдела учета услуг\n• Специалист по внедрению ПО SAP ERP\n\n*Общий стаж:* 16+ лет", parse_mode='Markdown')
    
    elif text == "🎓 Образование":
        await update.message.reply_text("🎓 **Образование:**\n\n*Высшее образование:*\nАкадемия экономики и права\nСпециальность: Менеджмент на производстве\n\n*Среднее специальное образование:*\nХабаровская Банковская Школа\nСпециальность: Специалист банковского дела", parse_mode='Markdown')
    
    elif text == "🛠 Навыки":
        await update.message.reply_text("🛠 **Навыки:**\n\n*Профессиональные:*\n• Технологический контроль подземных работ\n• Внедрение SAP ERP\n• Работа с клиентами\n• Бухгалтерский контроль\n\n*Технические:*\n• MS Office\n• Python\n• Искусственный интеллект\n• SAP ERP", parse_mode='Markdown')
    
    elif text == "🤖 Проекты ИИ":
        await update.message.reply_text("🤖 **Проекты с ИИ:**\n\n*Текущие направления:*\n• Оптимизация рабочих задач\n• Внедрение систем мониторинга\n• Обработка видео с объектов\n• Разработка систем контроля", parse_mode='Markdown')
    
    elif text == "📞 Контакты":
        await update.message.reply_text(
            "📞 **Контакты:**\n\n📧 Email: GolovinRV@suek.ru\n📱 Telegram: @CrazyRab1t\n💼 ID: 1290102754",
            parse_mode='Markdown',
            reply_markup=get_contacts_keyboard()
        )
    
    elif text == "📰 Консультант ИИ":
        user_id = update.message.from_user.id
        can_request, message = can_make_request(user_id)
        
        info_text = f"🤖 **Консультант ИИ**\n\n"
        
        if user_id == 1290102754:
            info_text += "👑 *Режим администратора* - неограниченные запросы\n\n"
        else:
            used_requests = len(user_requests.get(user_id, []))
            info_text += f"📊 *Лимиты:* {used_requests}/3 запросов сегодня\n\n"
        
        info_text += "✅ **Разрешенные темы:**\n• Угольная промышленность\n• Качество угля\n• Искусственный интеллект\n\nВыберите тему:"
        
        await update.message.reply_text(
            info_text,
            parse_mode='Markdown',
            reply_markup=get_ai_consultant_keyboard()
        )
    
    elif text == "🏭 Качество угля":
        user_id = update.message.from_user.id
        await update.message.reply_text("🔄 Консультирую по качеству угля...")
        answer = ask_yandex_gpt("Расскажи о качестве угля", user_id)
        await update.message.reply_text(answer, parse_mode='Markdown')
    
    elif text == "📊 Параметры угля":
        user_id = update.message.from_user.id
        await update.message.reply_text("🔄 Анализирую параметры угля...")
        answer = ask_yandex_gpt("Объясни параметры угля", user_id)
        await update.message.reply_text(answer, parse_mode='Markdown')
    
    elif text == "🚀 Развитие ИИ":
        user_id = update.message.from_user.id
        await update.message.reply_text("🔄 Анализирую развитие ИИ...")
        answer = ask_yandex_gpt("Развитие искусственного интеллекта", user_id)
        await update.message.reply_text(answer, parse_mode='Markdown')
    
    elif text == "🤖 Задать свой вопрос":
        user_id = update.message.from_user.id
        can_request, message = can_make_request(user_id)
        
        if not can_request:
            await update.message.reply_text(f"❌ **{message}**", parse_mode='Markdown')
            return
        
        user_questions[user_id] = True
        await update.message.reply_text(
            "💭 **Задайте ваш вопрос**\n\nТемы: угольная промышленность, качество угля, ИИ\n\nВведите ваш вопрос:",
            parse_mode='Markdown'
        )
    
    elif text == "🔙 Назад":
        await update.message.reply_text("Главное меню:", reply_markup=get_main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "email":
        await query.edit_message_text("📧 Email: GolovinRV@suek.ru")
    elif query.data == "telegram":
        await query.edit_message_text("📱 Telegram: @CrazyRab1t\n💼 ID: 1290102754")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Главное меню:", reply_markup=get_main_keyboard())

async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📞 **Контакты:**\n\n📧 Email: GolovinRV@suek.ru\n📱 Telegram: @CrazyRab1t\n💼 ID: 1290102754",
        parse_mode='Markdown',
        reply_markup=get_contacts_keyboard()
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Ошибка: {context.error}")

def main() -> None:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не установлен!")
        print("📝 Установите переменную BOT_TOKEN в настройках Render")
        return
    
    print(f"🔑 Токен получен, длина: {len(BOT_TOKEN)} символов")
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("contacts", contacts_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        application.post_init = set_bot_commands
        
        print("✅ Бот визитка Головина Романа запущен!")
        print("👑 Админ ID: 1290102754")
        print("📊 Лимит: 3 запроса в сутки")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()