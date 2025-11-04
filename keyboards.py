from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """Главная клавиатура меню"""
    keyboard = [
        ["🔍 Обо мне", "💼 Опыт работы"],
        ["🎓 Образование", "🛠 Навыки"],
        ["🤖 Проекты ИИ", "📞 Контакты"],
        ["📰 Консультант ИИ"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_contacts_keyboard():
    """Клавиатура для раздела контакты"""
    keyboard = [
        [InlineKeyboardButton("📧 Email", callback_data="email")],
        [InlineKeyboardButton("📱 Telegram", callback_data="telegram")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ai_consultant_keyboard():
    """Клавиатура для ИИ консультанта"""
    keyboard = [
        ["🏭 Угольная промышленность"],
        ["📊 Качество угля"], 
        ["🚀 Искусственный интеллект"],
        ["📋 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_back_to_consultant_keyboard():
    """Клавиатура для возврата в консультант"""
    keyboard = [
        ["🔙 Назад к темам"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)