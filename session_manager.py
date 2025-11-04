import time

class SessionManager:
    def __init__(self):
        self.user_sessions = {}
    
    def get_user_session(self, user_id):
        """Получает или создает сессию пользователя"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "consultant_topic": None,
                "waiting_for_question": False,
                "last_activity": time.time()
            }
        return self.user_sessions[user_id]
    
    def set_consultant_topic(self, user_id, topic):
        """Устанавливает тему консультанта для пользователя"""
        session = self.get_user_session(user_id)
        session["consultant_topic"] = topic
        session["waiting_for_question"] = False
        session["last_activity"] = time.time()
    
    def get_consultant_topic(self, user_id):
        """Получает текущую тему консультанта пользователя"""
        session = self.get_user_session(user_id)
        return session["consultant_topic"]
    
    def clear_consultant_topic(self, user_id):
        """Очищает тему консультанта"""
        session = self.get_user_session(user_id)
        session["consultant_topic"] = None
        session["waiting_for_question"] = False
        session["last_activity"] = time.time()
    
    def is_in_consultant_mode(self, user_id):
        """Проверяет, находится ли пользователь в режиме консультанта"""
        return self.get_consultant_topic(user_id) is not None

# Глобальный менеджер сессий
session_manager = SessionManager()