import os
import aiohttp
import logging
import asyncio

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
        base_prompt = """Ты - AI-консультант Романа Головина, старшего контрольного мастера подземным в компании "Ургалуголь" с 16-летним опытом работы. Отвечай профессионально, вежливо и информативно, основываясь на реальном опыте работы в угольной промышленности. Будь конкретен и давай практические рекомендации."""
        
        prompts = {
            "угольная_промышленность": f"""{base_prompt}
Ты консультант по угольной промышленности. Отвечай на вопросы о:
- Технологиях подземной добычи угля
- Горном оборудовании и технике
- Технике безопасности и охране труда
- Процессах обогащения угля
- Логистике и транспортировке
- Производственных процессах на шахтах
- Нормативах и стандартах отрасли""",

            "качество_угля": f"""{base_prompt}
Ты специалист по контролю качества угля. Консультируй по:
- Методам оценки качества угля
- Параметрам качества (зольность, влажность, теплота сгорания)
- Стандартам ГОСТ и техническим нормативам
- Лабораторным исследованиям и испытаниям
- Сертификации угольной продукции
- Контролю качества на всех этапах производства
- Маркировке и классификации угля""",

            "искусственный_интеллект": f"""{base_prompt}
Ты эксперт по внедрению искусственного интеллекта в промышленности. Консультируй по:
- Оптимизации производственных процессов с помощью ИИ
- Компьютерному зрению для мониторинга оборудования
- Predictive maintenance (прогнозное обслуживание)
- Анализу данных и аналитике
- Автоматизации рутинных операций
- Внедрению AI-решений в угольной отрасли
- Цифровой трансформации производства"""
        }
        
        return prompts.get(topic, base_prompt)
    
    async def ask_question(self, question, topic="угольная_промышленность"):
        """Отправляет вопрос в Yandex GPT и получает ответ"""
        if not self.is_configured():
            return "❌ Сервис AI-консультанта временно недоступен. Пожалуйста, попробуйте позже."
        
        try:
            headers = {
                "Authorization": f"Api-Key {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "modelUri": f"gpt://{self.folder_id}/yandexgpt/latest",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.3,
                    "maxTokens": 2000
                },
                "messages": [
                    {
                        "role": "system",
                        "text": self.get_system_prompt(topic)
                    },
                    {
                        "role": "user", 
                        "text": f"Вопрос: {question}\n\nПожалуйста, дай развернутый профессиональный ответ, основанный на реальном опыте работы в угольной промышленности. Будь конкретен и практичен."
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url, 
                    headers=headers, 
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        answer = result['result']['alternatives'][0]['message']['text']
                        return answer
                    else:
                        error_text = await response.text()
                        logger.error(f"Yandex GPT API error: {response.status} - {error_text}")
                        return "❌ Произошла ошибка при обращении к AI-консультанту. Пожалуйста, попробуйте еще раз."
                        
        except aiohttp.ClientError as e:
            logger.error(f"Network error: {e}")
            return "❌ Ошибка соединения с AI-консультантом. Проверьте подключение к интернету."
        except asyncio.TimeoutError:
            logger.error("Yandex GPT request timeout")
            return "❌ Превышено время ожидания ответа от AI-консультанта."
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "❌ Произошла непредвиденная ошибка. Пожалуйста, попробуйте еще раз."

# Создаем глобальный экземпляр
yandex_gpt = YandexGPT()