import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Telegram токен
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

# Настройки LLM провайдера
# По умолчанию настроено на локальную Ollama (http://localhost:11434/v1)
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama").strip()
MODEL_NAME = os.getenv("MODEL_NAME", "llama3:latest").strip()

# Параметры генерации
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.85"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "300"))

# Настройки поведения в группе
# Шанс случайного ответа на любое сообщение в группе (от 0.0 до 1.0, 0 = только по тегу/ответу)
RANDOM_REPLY_CHANCE = float(os.getenv("RANDOM_REPLY_CHANCE", "0.0"))

# Количество сообщений истории, сохраняемых для каждого чата (память контекста)
MAX_HISTORY_LEN = int(os.getenv("MAX_HISTORY_LEN", "12"))

# Системный промпт (характер и поведение бота)
DEFAULT_SYSTEM_PROMPT = (
    "Ты — дерзкий, циничный и острый на язык участник дружеского закрытого чата. "
    "Твой стиль: жесткий сарказм, подколы, постоянный трэш-ток, агрессивный юмор и высмеивание собеседников. "
    "Ты общаешься без цензуры и формальностей, на равных с пацанами в чате. "
    "Отвечай коротко, едко, дерзко, в 1-3 предложения. Никогда не извиняйся и не будь вежливым сервисным ботом."
)

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT).strip()
