# 🤖 TGBot — AI-Powered Telegram Message Summarizer

> Автоматическая система саммаризации сообщений из Telegram с использованием **GigaChat API** (Сбер) и веб-интерфейсом для мониторинга.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-blue.svg)](https://core.telegram.org/bots/api)

---

## 📖 О проекте

**TGBot** — это комплексная система для работы с Telegram-сообщениями:

🔹 **Автоматический сбор** сообщений из чатов через Telethon  
🔹 **AI-саммаризация** текстов через GigaChat (Сбер)  
🔹 **Telegram-бот** с удобными кнопками для управления  
🔹 **Веб-дашборд** (Flask) для мониторинга и статистики  
🔹 **Telegram Mini App** — встроенный интерфейс прямо в Telegram  
🔹 **Публикация в интернет** через CloudPub.ru (бесплатные туннели)

### 🎯 Основные возможности

- ✅ Сбор сообщений из Telegram-чатов в реальном времени
- ✅ Умная фильтрация (исключение команд, собственных сообщений бота)
- ✅ Саммаризация сообщений по команде через GigaChat AI
- ✅ База данных SQLite для хранения истории
- ✅ Веб-интерфейс с красивым дашбордом
- ✅ Telegram Mini App для доступа из мобильного приложения
- ✅ Временные метки в московском времени (MSK, UTC+3)
- ✅ Кнопочный интерфейс бота (без ручного ввода команд)

---

## 🏗️ Архитектура

```
┌─────────────────┐
│   Telegram      │ ← Пользователи пишут сообщения
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Telethon │ ← Собирает сообщения
    └────┬─────┘   (фильтрация команд/ботов)
         │
    ┌────▼─────────┐
    │ messages.db  │ ← SQLite база данных
    └────┬─────────┘
         │
    ┌────▼──────────┐
    │ Summary Bot   │ ← Команды: /status, /summary
    └────┬──────────┘   Кнопки: 📊 Статус, 📝 Саммаризация
         │
    ┌────▼─────────┐
    │  GigaChat AI │ ← Саммаризация текста
    └──────────────┘
         │
    ┌────▼──────────────────────┐
    │  Flask Dashboard (5000)   │ ← Статистика
    │  Mini App (5001)          │ ← Telegram Mini App
    └───────────────────────────┘
         │
    ┌────▼──────────┐
    │  CloudPub.ru  │ ← Публикация в интернет
    └───────────────┘
```

---

## 🚀 Быстрый старт

### 📋 Требования

- **Python 3.10+**
- **Telegram Bot Token** — получите у [@BotFather](https://t.me/BotFather)
- **GigaChat API credentials** — [зарегистрируйтесь](https://developers.sber.ru/portal/products/gigachat)
- **Telethon API** — получите на [my.telegram.org](https://my.telegram.org/apps)

### ⚙️ Установка

#### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-username/TGBot.git
cd TGBot
```

#### 2. Создайте виртуальное окружение

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

#### 4. Настройте конфигурацию

Скопируйте `env.example` в `.env` и заполните своими данными:

```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
bot_username=YourBotUsername

# Telethon (для сбора сообщений)
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=tg_session

# GigaChat API
CLIENT_ID=your_gigachat_client_id
CLIENT_SECRET=your_gigachat_client_secret
GIGACHAT_CA_BUNDLE=certs/giga_chain.pem

# CloudPub (опционально, для публикации в интернет)
CLOUDPUB_EMAIL=your@email.com
CLOUDPUB_PASSWORD=your_password
```

#### 5. Получите SSL-сертификаты GigaChat

**Windows:**
```powershell
.\certs\fetch_gigachat_cert.ps1
```

**Linux/macOS:**
```bash
mkdir -p certs
openssl s_client -showcerts -connect ngw.devices.sberbank.ru:9443 </dev/null 2>/dev/null | \
  openssl x509 -outform PEM > certs/giga_chain.pem
```

---

## 🎮 Использование

### Запуск компонентов

**1. Telethon — сбор сообщений:**
```bash
python telethon/main.py
```

**2. Summary Bot — Telegram-бот:**
```bash
python telebot/summary_bot.py
```

**3. Flask Dashboard — веб-интерфейс (порт 5000):**
```bash
python flask/app.py
```
Откройте: http://localhost:5000

**4. Telegram Mini App (порт 5001):**
```bash
python miniapp/app.py
```

### 📱 Использование бота в Telegram

Отправьте боту команды или нажмите кнопки:

- **📊 Статус** (`/status`) — количество необработанных сообщений
- **📝 Саммаризация** (`/summary`) — получить краткую сводку всех новых сообщений

---

## 🌐 Публикация в интернет (CloudPub.ru)

Для доступа к веб-интерфейсам из интернета используйте CloudPub.

### Вариант A: CloudPub CLI (простой)

```bash
# Установка (если нужна)
# Скачайте с https://cloudpub.ru/download

# Авторизация
clo login

# Регистрация туннелей
clo register http 5000  # Flask Dashboard
clo register http 5001  # Mini App

# Запуск
clo run
```

**Автоматический запуск:**
```powershell
# Windows
.\start_tunnels_simple.ps1

# Linux/macOS/Windows
python start_tunnels.py
```

### Вариант B: Python SDK (продвинутый)

```bash
# Установка
pip install cloudpub-python-sdk

# Запуск
python start_tunnels_sdk.py
```

📖 **Подробная документация:**
- [CLOUDPUB_SETUP.md](CLOUDPUB_SETUP.md) — полная инструкция
- [CLOUDPUB_CLI_VS_SDK.md](CLOUDPUB_CLI_VS_SDK.md) — сравнение CLI и SDK

---

## 📁 Структура проекта

```
TGBot/
├── 📂 ai/                      # GigaChat API интеграция
│   ├── gigachat.py            # OAuth и саммаризация
│   └── README.md
├── 📂 telethon/                # Сбор сообщений из Telegram
│   ├── main.py                # Клиент Telethon
│   ├── db.py                  # Работа с БД
│   └── README.md
├── 📂 telebot/                 # Telegram-бот
│   ├── summary_bot.py         # Команды и кнопки
│   └── README.md
├── 📂 flask/                   # Веб-интерфейс (порт 5000)
│   ├── app.py
│   ├── templates/
│   └── README.md
├── 📂 miniapp/                 # Telegram Mini App (порт 5001)
│   ├── app.py
│   ├── templates/
│   └── README.md
├── 📂 certs/                   # SSL-сертификаты GigaChat
├── 📂 scripts/                 # Вспомогательные скрипты
├── start_tunnels.py           # Запуск туннелей (CLI)
├── start_tunnels_sdk.py       # Запуск туннелей (SDK)
├── start_tunnels_simple.ps1   # PowerShell скрипт туннелей
├── check_status.py            # Проверка статуса системы
├── .env                       # Конфигурация (не в Git)
├── env.example                # Пример конфигурации
├── requirements.txt           # Зависимости Python
└── messages.db                # База данных (не в Git)
```

---

## 📚 Документация

### 📖 Основные руководства

| Документ | Описание |
|----------|----------|
| [README.md](README.md) | Этот файл — краткий обзор |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | 🚀 **Полное руководство по развертыванию** |
| [PROJECT_HISTORY.md](PROJECT_HISTORY.md) | История разработки, решённые проблемы |
| [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) | Справочник всех команд |
| [CHANGELOG.md](CHANGELOG.md) | История изменений |

### 🌐 CloudPub (публикация в интернет)

| Документ | Описание |
|----------|----------|
| [CLOUDPUB_CLI_VS_SDK.md](CLOUDPUB_CLI_VS_SDK.md) | 🌟 **CLI vs Python SDK** |
| [CLOUDPUB_SETUP.md](CLOUDPUB_SETUP.md) | Подробная настройка |
| [QUICKSTART_CLOUDPUB.txt](QUICKSTART_CLOUDPUB.txt) | Краткая памятка |
| [CLOUDPUB_COMMANDS.txt](CLOUDPUB_COMMANDS.txt) | Справочник команд CLI |

### 🔧 Модули проекта

- [ai/README.md](ai/README.md) — GigaChat API
- [telethon/README.md](telethon/README.md) — Сбор сообщений
- [telebot/README.md](telebot/README.md) — Telegram-бот
- [flask/README.md](flask/README.md) — Веб-интерфейс
- [miniapp/README.md](miniapp/README.md) — Mini App

---

## 🐛 Решение проблем

### Telegram Bot: 409 Conflict Error

Если бот выдаёт ошибку "Conflict: terminated by other getUpdates request":

```bash
# Удалите webhook
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook?drop_pending_updates=true"
```

### GigaChat: SSL Certificate Error

Убедитесь, что сертификаты загружены:

```bash
# Windows
.\certs\fetch_gigachat_cert.ps1

# Linux/macOS
openssl s_client -showcerts -connect ngw.devices.sberbank.ru:9443 </dev/null 2>/dev/null | \
  openssl x509 -outform PEM > certs/giga_chain.pem
```

### Проверка базы данных

```python
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM messages WHERE summarized = 0'); print('Необработанных:', cursor.fetchone()[0]); conn.close()"
```

### Проверка статуса всех компонентов

```bash
python check_status.py
```

---

## 🤝 Вклад в проект

Приветствуются любые улучшения! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## 📄 Лицензия

Этот проект распространяется под лицензией **MIT License** — см. файл [LICENSE](LICENSE).

---

## 🙏 Благодарности

- **[GigaChat](https://developers.sber.ru/portal/products/gigachat)** — AI-саммаризация от Сбера
- **[Telethon](https://github.com/LonamiWebs/Telethon)** — работа с Telegram MTProto API
- **[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)** — Telegram Bot API
- **[Flask](https://flask.palletsprojects.com/)** — веб-фреймворк
- **[CloudPub.ru](https://cloudpub.ru)** — бесплатные туннели

---

## 📞 Контакты

Если у вас есть вопросы или предложения, создайте [Issue](../../issues) в репозитории.

---

**⭐ Если проект оказался полезен, поставьте звезду!**

