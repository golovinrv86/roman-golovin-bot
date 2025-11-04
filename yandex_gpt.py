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
            "угольная_промышленность": """Ты консультант по угольной промышленности с 16-летним опытом работы в компании "Ургалуголь". Отвечай профессионально на вопросы о технологиях добычи угля, оборудовании, технике безопасности, процессах обогащения и логистике.""",

            "качество_угля": """Ты специалист по контролю качества угля. Отвечай на вопросы о методах оценки качества, параметрах качества (зольность, влажность, теплота сгорания), стандартах, лабораторных исследованиях и сертификации продукции.""",

            "искусственный_интеллект": """Ты эксперт по внедрению искусственного интеллекта в промышленности. Консультируй по оптимизации процессов, компьютерному зрению, predictive maintenance и анализу данных."""
        }
        
        return prompts.get(topic, """Ты AI-консультант Романа Головина. Отвечай на вопросы профессионально и вежливо.""")
    
    async def ask_question(self, question, topic="общий"):
        """Отправляет вопрос в Yandex GPT и возвращает ответ"""
        
        if not self.is_configured():
            error_msg = "❌ Сервис консультанта временно недоступен. Ведутся технические работы."
            print(f"Yandex GPT не настроен: API_KEY={bool(self.api_key)}, FOLDER_ID={bool(self.folder_id)}")
            return error_msg
        
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
            
            print(f"🔄 Отправляем запрос в Yandex GPT: {question[:50]}...")
            
            response = requests.post(self.url, headers=headers, json=data, timeout=30)
            
            print(f"📨 Получен ответ: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result and "alternatives" in result["result"]:
                    answer = result["result"]["alternatives"][0]["message"]["text"]
                    print(f"✅ Успешный ответ от Yandex GPT: {answer[:100]}...")
                    return answer
                else:
                    error_msg = "❌ Неверный формат ответа от сервиса."
                    print(f"Ошибка формата ответа: {result}")
                    return error_msg
            else:
                error_msg = f"⚠️ Ошибка сервиса (код {response.status_code}). Попробуйте позже."
                logger.error(f"Yandex GPT API error: {response.status_code} - {response.text}")
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return error_msg
                
        except requests.exceptions.Timeout:
            error_msg = "⏰ Сервис не отвечает. Попробуйте задать вопрос позже."
            print("Таймаут запроса к Yandex GPT")
            return error_msg
        except requests.exceptions.ConnectionError:
            error_msg = "🔌 Проблемы с соединением. Проверьте интернет."
            print("Ошибка соединения с Yandex GPT")
            return error_msg
        except Exception as e:
            error_msg = "❌ Произошла непредвиденная ошибка. Попробуйте еще раз."
            logger.error(f"Error in Yandex GPT: {e}")
            print(f"Неожиданная ошибка: {e}")
            return error_msg

# Создаем глобальный экземпляр
yandex_gpt = YandexGPT()