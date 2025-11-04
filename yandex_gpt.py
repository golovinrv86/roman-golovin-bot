import os
import requests
import logging
import json

logger = logging.getLogger(__name__)

class YandexGPT:
    def __init__(self):
        self.api_key = os.environ.get('YANDEX_GPT_API_KEY')
        self.folder_id = os.environ.get('YANDEX_FOLDER_ID')
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
    def is_configured(self):
        """Проверяет, настроены ли ключи API"""
        return bool(self.api_key and self.folder_id)
    
    def get_system_prompt(self, topic):
        """Возвращает системный промпт в зависимости от темы"""
        prompts = {
            "угольная_промышленность": """Ты консультант по угольной промышленности. Отвечай как опытный специалист с 16-летним стажем в компании "Ургалуголь". 
            
Основные темы для консультаций:
- Технологии добычи угля
- Контроль качества угля
- Процессы обогащения
- Логистика и транспортировка
- Техника безопасности
- Оборудование для добычи

Отвечай профессионально, но доступно. Используй примеры из реальной практики.""",

            "качество_угля": """Ты специалист по контролю качества угля. Отвечай на вопросы о:
- Методах оценки качества угля
- Параметрах качества (зольность, влажность, теплота сгорания)
- Стандартах и нормативах
- Лабораторных исследованиях
- Сертификации продукции

Будь точным в технических деталях, но объясняй простым языком.""",

            "искусственный_интеллект": """Ты эксперт по внедрению искусственного интеллекта в промышленности. Консультируй по:
- Оптимизации производственных процессов с помощью ИИ
- Компьютерному зрению для мониторинга
- Predictive maintenance
- Анализу данных в реальном времени
- ROI от внедрения ИИ-решений

Делись практическим опытом внедрения."""
        }
        
        return prompts.get(topic, """Ты AI-консультант Романа Головина. Отвечай на вопросы профессионально и вежливо. 
Если вопрос не по теме, вежливо предложи выбрать одну из доступных тем консультации.""")

    async def ask_question(self, question, topic="общий"):
        """Отправляет вопрос в Yandex GPT и возвращает ответ"""
        
        if not self.is_configured():
            return "❌ Сервис консультанта временно недоступен. Ведутся технические работы."
        
        try:
            headers = {
                "Authorization": f"Api-Key {self.api_key}",
                "Content-Type": "application/json"
            }
            
            system_prompt = self.get_system_prompt(topic)
            
            data = {
                "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.3,
                    "maxTokens": 2000
                },
                "messages": [
                    {
                        "role": "system",
                        "text": system_prompt
                    },
                    {
                        "role": "user", 
                        "text": question
                    }
                ]
            }
            
            response = requests.post(self.url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                answer = result["result"]["alternatives"][0]["message"]["text"]
                return answer
            else:
                logger.error(f"Yandex GPT API error: {response.status_code} - {response.text}")
                return "⚠️ Произошла ошибка при обращении к сервису. Попробуйте позже."
                
        except requests.exceptions.Timeout:
            return "⏰ Сервис не отвежает. Попробуйте задать вопрос позже."
        except Exception as e:
            logger.error(f"Error in Yandex GPT: {e}")
            return "❌ Произошла непредвиденная ошибка. Попробуйте еще раз."

# Создаем глобальный экземпляр
yandex_gpt = YandexGPT()