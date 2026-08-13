import logging
from typing import List, Dict
from openai import AsyncOpenAI
import config

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=config.LLM_BASE_URL,
            api_key=config.LLM_API_KEY
        )
        self.model = config.MODEL_NAME
        self.temperature = config.TEMPERATURE
        self.max_tokens = config.MAX_TOKENS

    async def generate_reply(self, messages: List[Dict[str, str]]) -> str:
        """Отправляет контекст сообщений в LLM и возвращает сгенерированный ответ."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            reply = response.choices[0].message.content
            if not reply:
                return "..."
            return reply.strip()
        except Exception as e:
            logger.error(f"Ошибка вызова LLM API ({self.model} @ {config.LLM_BASE_URL}): {e}", exc_info=True)
            return f"⚠️ Ошибка генерации нейросети: {e}"

llm_service = LLMService()
