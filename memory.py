from collections import defaultdict, deque
from typing import List, Dict
import config

class ChatMemory:
    """Управление краткосрочной памятью диалогов для каждого чата."""
    def __init__(self, max_len: int = config.MAX_HISTORY_LEN):
        self.max_len = max_len
        self._history: Dict[int, deque] = defaultdict(lambda: deque(maxlen=self.max_len))

    def add_user_message(self, chat_id: int, user_name: str, text: str):
        """Добавляет сообщение пользователя в историю."""
        self._history[chat_id].append({
            "role": "user",
            "content": f"{user_name}: {text}"
        })

    def add_assistant_message(self, chat_id: int, bot_name: str, text: str):
        """Добавляет ответ бота в историю."""
        self._history[chat_id].append({
            "role": "assistant",
            "content": text
        })

    def get_messages(self, chat_id: int, system_prompt: str) -> List[Dict[str, str]]:
        """Формирует список сообщений для передачи в LLM API."""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(list(self._history[chat_id]))
        return messages

    def clear(self, chat_id: int):
        """Очищает историю конкретного чата."""
        if chat_id in self._history:
            self._history[chat_id].clear()

# Глобальный синглтон памяти
chat_memory = ChatMemory()
