import sys
import random
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction

import config
from memory import chat_memory
from llm_service import llm_service

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("tg_banter_bot")

if not config.TELEGRAM_BOT_TOKEN:
    logger.error("ОШИБКА: TELEGRAM_BOT_TOKEN не задан! Заполните файл .env перед запуском.")
    sys.exit(1)

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Кэш информации о боте
bot_user: types.User = None

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработчик команды /start."""
    await message.reply(
        "Здарова. Я бот для вашего чата. Добавь меня в группу, тегай или отвечай на мои сообщения — поговорим по понятиям."
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Справка по командам."""
    help_text = (
        "📌 *Команды бота:*\n"
        "• `/start` — Запуск и приветствие\n"
        "• `/clear` — Очистить память диалога в этом чате\n"
        "• `/status` — Проверить настройки и подключение модели\n"
        "• `/help` — Эта справка\n\n"
        "💬 *Как общаться:*\n"
        "— В личке: просто пиши любое сообщение.\n"
        "— В группе: тегай меня (`@имя_бота`) или отвечай (Reply) на мои сообщения."
    )
    await message.reply(help_text, parse_mode="Markdown")

@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    """Очистить историю контекста в текущем чате."""
    chat_memory.clear(message.chat.id)
    await message.reply("🧹 Память чата очищена. Начинаем с чистого листа.")

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    """Проверка текущего статуса и активной модели."""
    status_text = (
        f"⚙️ *Статус бота:*\n"
        f"• Модель: `{config.MODEL_NAME}`\n"
        f"• LLM Сервер: `{config.LLM_BASE_URL}`\n"
        f"• Температура: `{config.TEMPERATURE}`\n"
        f"• Память чата: `{config.MAX_HISTORY_LEN}` сообщений\n"
        f"• Случайный ответ: `{int(config.RANDOM_REPLY_CHANCE * 100)}%`"
    )
    await message.reply(status_text, parse_mode="Markdown")

@dp.message(F.text)
async def handle_message(message: types.Message):
    """Основной обработчик текстовых сообщений."""
    global bot_user
    if not bot_user:
        bot_user = await bot.get_me()

    chat_id = message.chat.id
    user_name = message.from_user.full_name or message.from_user.first_name or "Аноним"
    text = message.text.strip()

    # Проверка, является ли чат личным
    is_private = message.chat.type == "private"

    # Проверка, упомянут ли бот тегом @username
    bot_mention = f"@{bot_user.username}" if bot_user.username else ""
    is_mentioned = bot_mention in text if bot_mention else False

    # Проверка, является ли сообщение ответом (Reply) на сообщение бота
    is_reply_to_bot = (
        message.reply_to_message is not None and
        message.reply_to_message.from_user is not None and
        message.reply_to_message.from_user.id == bot_user.id
    )

    # Случайный триггер в группе
    random_trigger = False
    if not is_private and config.RANDOM_REPLY_CHANCE > 0:
        random_trigger = random.random() < config.RANDOM_REPLY_CHANCE

    # Всегда сохраняем сообщение в историю чата для поддержания контекста
    chat_memory.add_user_message(chat_id, user_name, text)

    # Решаем, должен ли бот ответить
    should_reply = is_private or is_mentioned or is_reply_to_bot or random_trigger

    if not should_reply:
        return

    # Очищаем текст от тега бота для передачи в модель
    clean_text = text.replace(bot_mention, "").strip() if bot_mention else text

    # Показываем статус "печатает..." в чате
    try:
        await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    except Exception:
        pass

    # Получаем историю сообщений с системным промптом
    messages_payload = chat_memory.get_messages(chat_id, config.SYSTEM_PROMPT)

    # Запрашиваем ответ у нейросети
    reply_text = await llm_service.generate_reply(messages_payload)

    # Сохраняем ответ бота в память
    chat_memory.add_assistant_message(chat_id, bot_user.first_name, reply_text)

    # Отправляем ответ в Telegram
    try:
        await message.reply(reply_text)
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение в чат {chat_id}: {e}")
        try:
            await bot.send_message(chat_id=chat_id, text=reply_text)
        except Exception as e2:
            logger.error(f"Критическая ошибка отправки: {e2}")

async def main():
    global bot_user
    bot_user = await bot.get_me()
    logger.info(f"Бот успешно запущен: @{bot_user.username} (ID: {bot_user.id})")
    logger.info(f"Подключение к LLM: {config.LLM_BASE_URL} | Модель: {config.MODEL_NAME}")
    
    # Удаляем вебхуки, если они были установлены, и запускаем long polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
