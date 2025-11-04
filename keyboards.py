from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = [
        ["🔍 Обо мне", "💼 Опыт работы"],
        ["🎓 Образование", "🛠 Навыки"],
        ["🤖 Проекты ИИ", "📞 Контакты"],
        ["📰 Консультант ИИ"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_contacts_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📧 Email", callback_data="email"),
            InlineKeyboardButton("📱 Telegram", callback_data="telegram")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ai_consultant_keyboard():
    keyboard = [
        ["🏭 Качество угля", "📊 Параметры угля"],
        ["🚀 Развитие ИИ", "🤖 Задать свой вопрос"],
        ["🔙 Назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)