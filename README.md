# 🤖 Telegram Banter / Roast Бот с ИИ

Готовый бот для групповых чатов Telegram с поддержкой кастомного дерзкого характера и интеграцией с любой языковой моделью через OpenAI-совместимый API (включая локальную бесплатную **Ollama** без облачной цензуры, **OpenRouter**, **DeepSeek** и др.).

---

## 📁 Структура проекта

- [`bot.py`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/bot.py) — основной файл логики бота на `aiogram 3`.
- [`llm_service.py`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/llm_service.py) — модуль отправки запросов в нейросеть.
- [`memory.py`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/memory.py) — память контекста диалога по чатам.
- [`config.py`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/config.py) — загрузка настроек из `.env`.
- [`.env`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/.env) — конфигурационный файл (токены, промпты, URL нейросети).
- [`requirements.txt`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/requirements.txt) — список библиотек.
- [`run.bat`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/run.bat) — файл запуска в 1 клик для Windows.

---

## 🚀 Пошаговая инструкция по настройке

### Шаг 1. Создание бота в Telegram
1. Откройте в Telegram официального бота **[@BotFather](https://t.me/BotFather)**.
2. Отправьте команду `/newbot`.
3. Укажите имя бота (например, `Пацанский Бот`) и юзернейм (например, `super_roast_chat_bot`).
4. Скопируйте выданный **HTTP API токен** (вида `1234567890:ABCdef...`).

### Шаг 2. Настройка приватности для групп (Обязательно!)
Чтобы бот мог видеть сообщения в группе при ответах и упоминаниях:
1. В диалоге с `@BotFather` введите `/mybots` и выберите вашего бота.
2. Перейдите в раздел **Bot Settings** ➔ **Group Privacy**.
3. Нажмите **Turn off** (статус должен стать `Privacy mode is disabled`).
4. Также в разделе **Bot Settings** ➔ **Allow Groups?** убедитесь, что группы включены (`Groups are enabled`).

---

### Шаг 3. Выбор и запуск нейросети (LLM)

#### Вариант А: Локально через Ollama (Бесплатно, без ограничений и цензуры)
1. Скачайте и установите [Ollama](https://ollama.com).
2. Откройте терминал / PowerShell и скачайте желаемую модель:
   ```bash
   ollama run llama3
   ```
   *(или `ollama run mistral` / `ollama run qwen2.5:7b`)*
3. Ollama автоматически запустит локальный сервер на `http://localhost:11434/v1`.

#### Вариант Б: Облачный API (OpenRouter, DeepSeek и др.)
Если не хотите нагружать свой компьютер, можно использовать облачные сервисы:
- **OpenRouter**: зарегистрируйтесь на [openrouter.ai](https://openrouter.ai), пополните баланс и возьмите API-ключ.
- Укажите в `.env`:
  ```env
  LLM_BASE_URL="https://openrouter.ai/api/v1"
  LLM_API_KEY="ваш_ключ_openrouter"
  MODEL_NAME="mistralai/mistral-nemo"
  ```

---

### Шаг 4. Настройка файла `.env`
Откройте файл [`.env`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/.env) и вставьте ваш токен Telegram:
```env
TELEGRAM_BOT_TOKEN="1234567890:ABCdef_ваш_токен_от_BotFather"
```

Здесь же вы можете изменить `SYSTEM_PROMPT` под желаемый стиль и характер бота.

---

### Шаг 5. Запуск бота
- На Windows просто дважды кликните на **[`run.bat`](file:///C:/Users/jamsen/.gemini/antigravity/scratch/tg-banter-bot/run.bat)**. Скрипт сам создаст виртуальное окружение, установит зависимости и запустит бота.
- Либо вручную через консоль:
  ```bash
  pip install -r requirements.txt
  python bot.py
  ```

---

## 👥 Использование в группе

1. Добавьте созданного бота в ваш Telegram-чат с друзьями.
2. Бот отвечает:
   - При прямом упоминании (`@имя_бота привет`);
   - При ответе (Reply) на любое сообщение бота;
   - В личных сообщениях — на любое сообщение;
   - (Опционально) На случайные сообщения в группе, если в `.env` параметр `RANDOM_REPLY_CHANCE` установлен больше `0` (например `0.1` = 10% шанс).
