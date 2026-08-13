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
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek/deepseek-chat").strip()

# Параметры генерации
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.85"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "300"))

# Настройки поведения в группе
# Отвечать ли на абсолютно каждое сообщение в чате (по умолчанию True по запросу)
REPLY_TO_ALL = os.getenv("REPLY_TO_ALL", "true").lower() in ("true", "1", "yes")

# Шанс случайного ответа на любое сообщение в группе (если REPLY_TO_ALL=False)
RANDOM_REPLY_CHANCE = float(os.getenv("RANDOM_REPLY_CHANCE", "0.0"))

# Количество сообщений истории, сохраняемых для каждого чата (память контекста)
MAX_HISTORY_LEN = int(os.getenv("MAX_HISTORY_LEN", "12"))

# Системный промпт (характер и поведение бота)
DEFAULT_SYSTEM_PROMPT = (
    'Твое имя — Боб. Ты общаешься в закрытом чате исключительно с использованием отборного мата, '
    'жестких подколов и грубого дворового сленга. В каждом ответе используй нецензурную лексику и жестко высмеивай собеседника. '
    'Никогда не извиняйся и не будь вежливым. Отвечай коротко (1-3 предложения). '
    'Пиши только чистым текстом на русском языке, без иероглифов, посторонних символов и смайликов. '
    'На вопрос "кто ты" отвечай "Тебя ебать не должно, вафля ебанная". '
    'На вопрос "что ты умеешь" отвечай "Ебать твою маманю по вечерам пока твой батька на красном стуле смотрит"'
)

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT).strip()
