# 🚀 Полное руководство по развертыванию TGBot проекта

Это пошаговое руководство по развертыванию всей системы саммаризации Telegram-сообщений.

---

## 📋 Содержание

1. [Требования](#требования)
2. [Установка зависимостей](#установка-зависимостей)
3. [Настройка конфигурации](#настройка-конфигурации)
4. [Запуск компонентов](#запуск-компонентов)
5. [Публикация в интернет](#публикация-в-интернет)
6. [Настройка Mini App](#настройка-mini-app)
7. [Проверка работы](#проверка-работы)
8. [Решение проблем](#решение-проблем)

---

## 📦 Требования

### Системные требования
- Windows 10/11 (или Linux/macOS)
- Python 3.10 или выше
- PowerShell (для Windows)
- 500 МБ свободного места

### Необходимые учетные записи
- ✅ Telegram аккаунт
- ✅ GigaChat API доступ (https://developers.sber.ru/)
- ✅ Telegram Bot Token (от @BotFather)
- ✅ Telethon API credentials (https://my.telegram.org/apps)
- ⭕ CloudPub.ru аккаунт (опционально, для публикации)

---

## 🔧 Установка зависимостей

### Шаг 1: Клонирование или распаковка проекта

Если проект уже на USB-диске:
```powershell
cd F:\Zerocoder\Intensive\TGBot
```

### Шаг 2: Создание виртуального окружения

```powershell
python -m venv .venv
```

### Шаг 3: Активация окружения

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.\.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### Шаг 4: Установка Python пакетов

```powershell
pip install -r requirements.txt
```

Установка займет 2-5 минут в зависимости от скорости интернета.

---

## ⚙️ Настройка конфигурации

### Шаг 1: Создание файла .env

Скопируйте шаблон:
```powershell
copy env.example .env
```

### Шаг 2: Получение GigaChat credentials

1. Перейдите на https://developers.sber.ru/
2. Зарегистрируйтесь / войдите
3. Создайте новый проект
4. Получите **Client ID** и **Client Secret**

### Шаг 3: Создание Telegram бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям (выберите имя и username)
4. Скопируйте **Bot Token**

### Шаг 4: Получение Telethon API credentials

1. Перейдите на https://my.telegram.org/apps
2. Войдите с помощью вашего номера телефона
3. Создайте новое приложение
4. Скопируйте **API ID** и **API Hash**

### Шаг 5: Заполнение .env файла

Откройте `.env` в текстовом редакторе и заполните:

```env
# GigaChat API
GIGACHAT_CLIENT_ID=ваш_client_id_здесь
GIGACHAT_CLIENT_SECRET=ваш_client_secret_здесь

# Telegram Bot
BOT_TOKEN=ваш_bot_token_здесь

# Telethon (для сбора сообщений)
API_ID=ваш_api_id_здесь
API_HASH=ваш_api_hash_здесь
```

**⚠️ Важно:** Не делитесь этим файлом с другими!

---

## 🚀 Запуск компонентов

### Рекомендуемый порядок запуска

Откройте **4 терминала** (или вкладки в IDE):

#### Терминал 1: Telethon (сбор сообщений)

```powershell
cd F:\Zerocoder\Intensive\TGBot
.\.venv\Scripts\Activate.ps1
python telethon\main.py
```

При первом запуске потребуется авторизация:
1. Введите номер телефона
2. Введите код из Telegram
3. (Опционально) Введите 2FA пароль

#### Терминал 2: Summary Bot (Telegram бот)

```powershell
cd F:\Zerocoder\Intensive\TGBot
.\.venv\Scripts\Activate.ps1
python telebot\summary_bot.py
```

#### Терминал 3: Flask Dashboard (веб-интерфейс)

```powershell
cd F:\Zerocoder\Intensive\TGBot
.\.venv\Scripts\Activate.ps1
python flask\app.py
```

Откройте в браузере: http://localhost:5000

#### Терминал 4: Telegram Mini App

```powershell
cd F:\Zerocoder\Intensive\TGBot
.\.venv\Scripts\Activate.ps1
python miniapp\app.py
```

Откройте в браузере: http://localhost:5001

### ✅ Проверка запуска

Все 4 компонента должны работать без ошибок. Проверьте:

```powershell
python check_status.py
```

---

## 🌐 Публикация в интернет

Для использования Mini App в Telegram нужно сделать его доступным из интернета.

### Вариант 1: Автоматический запуск через CloudPub

#### 1. Установка CloudPub

1. Перейдите на https://cloudpub.ru
2. Зарегистрируйтесь
3. Скачайте клиент для вашей ОС
4. Установите

#### 2. Авторизация

```powershell
clo login
```

Или:
```powershell
clo set token <ваш_токен_из_личного_кабинета>
```

#### 3. Запуск туннелей

**Автоматически (рекомендуется):**
```powershell
.\start_tunnels.ps1
```

**Вручную:**
```powershell
clo register http 5000
clo register http 5001
clo run
```

Вы получите 2 URL:
- `https://xxxxx.cloudpub.site` — Flask Dashboard (порт 5000)
- `https://yyyyy.cloudpub.site` — Mini App (порт 5001)

### Вариант 2: Использование ngrok

```powershell
ngrok http 5001
```

### Вариант 3: Собственный VPS

Если у вас есть VPS с белым IP, настройте Nginx/Apache для проксирования.

📖 **Подробная инструкция:** [CLOUDPUB_SETUP.md](CLOUDPUB_SETUP.md)

---

## 📱 Настройка Mini App в Telegram

После запуска туннелей:

### Шаг 1: Копирование URL

Скопируйте URL Mini App (порт 5001), например:
```
https://yyyyy.cloudpub.site
```

### Шаг 2: Настройка в @BotFather

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду: `/mybots`
3. Выберите вашего бота
4. Нажмите **Bot Settings**
5. Нажмите **Menu Button**
6. Нажмите **Edit Menu Button URL**
7. Вставьте скопированный URL
8. Нажмите **Change Menu Button Text** (опционально)
9. Введите текст кнопки, например: "📊 Статистика"

### Шаг 3: Проверка

1. Откройте вашего бота в Telegram
2. Нажмите на кнопку меню (≡) внизу экрана
3. Должно открыться Mini App с дашбордом

---

## ✅ Проверка работы

### 1. Проверка компонентов

```powershell
python check_status.py
```

Должно показать:
- ✅ База данных: OK
- ✅ Flask Dashboard: Запущен (порт 5000)
- ✅ Telegram Mini App: Запущен (порт 5001)
- ✅ CloudPub CLI: Установлен
- ✅ CloudPub: Авторизован

### 2. Проверка базы данных

```powershell
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM messages'); print('Всего сообщений:', cursor.fetchone()[0]); conn.close()"
```

### 3. Проверка Telegram бота

Откройте вашего бота в Telegram и отправьте:
- `📊 Статус` — должен показать количество необработанных сообщений
- `📝 Саммаризация` — должен создать саммаризацию

### 4. Проверка Flask Dashboard

Откройте http://localhost:5000 в браузере:
- Должна отображаться статистика
- Должны быть карточки с количеством сообщений
- Список сообщений должен обновляться

### 5. Проверка Mini App

Откройте вашего бота в Telegram и нажмите кнопку меню:
- Должно открыться Mini App
- Интерфейс должен быть адаптивным
- Данные должны совпадать с Flask Dashboard

---

## 🐛 Решение проблем

### Ошибка 409 Conflict (Telegram Bot)

**Причина:** Несколько инстансов бота запущено одновременно.

**Решение:**
```powershell
Invoke-WebRequest -Uri "https://api.telegram.org/bot<ВАШ_ТОКЕН>/deleteWebhook?drop_pending_updates=true"
```

Затем перезапустите бота.

### Database is locked (SQLite)

**Причина:** Несколько процессов пытаются писать в БД одновременно.

**Решение:**
```powershell
# Остановите все Python процессы
taskkill /F /IM python.exe

# Перезапустите компоненты по очереди
```

### GigaChat не отвечает

**Причина:** Истек токен доступа.

**Решение:**
```powershell
python scripts/update_token.py
```

### CloudPub туннели не работают

**Проверьте:**
1. Установлен ли CloudPub CLI: `clo --version`
2. Авторизованы ли вы: `clo options` (должен показать token)
3. Запущены ли приложения (Flask/Mini App)

**Решение:**
```powershell
# Авторизация
clo login

# Перезапуск туннелей
clo register http 5000
clo register http 5001
clo run
```

### Mini App не открывается в Telegram

**Проверьте:**
1. URL начинается с `https://` (HTTP не поддерживается)
2. Туннель активен и работает
3. Mini App запущен (порт 5001)
4. URL правильно настроен в @BotFather

### Сообщения не попадают в БД

**Проверьте:**
1. Telethon запущен: `python telethon\main.py`
2. Сессия авторизована (файл `tg_session.session` существует)
3. В логах Telethon нет ошибок

**Решение:**
- Перезапустите Telethon
- Проверьте права доступа к `messages.db`

---

## 📊 Архитектура системы

```
┌─────────────────────────────────────────────────────────────┐
│                        Telegram                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Пользователь │  │  Каналы      │  │  Summary Bot │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────────┐
│                      Telethon Client                         │
│              (Собирает сообщения)                            │
└─────────┬────────────────────────────────────────────────────┘
          │
          │ Сохраняет в БД
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│                    (messages.db)                             │
└─────────┬───────────────────────────┬───────────────────────┘
          │                           │
          │ Читает                    │ Читает
          │                           │
┌─────────▼───────────┐     ┌─────────▼───────────┐
│   Summary Bot       │     │   Flask Dashboard   │
│   (саммаризация)    │     │   (веб-интерфейс)   │
└─────────┬───────────┘     └─────────────────────┘
          │                           │
          │ Вызывает                  │ Публикуется
          ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐
│   GigaChat API      │     │   CloudPub Tunnel   │
│   (саммаризация)    │     │   (https://)        │
└─────────────────────┘     └─────────┬───────────┘
                                      │
                                      │ Открывается в
                                      ▼
                            ┌─────────────────────┐
                            │ Telegram Mini App   │
                            │ (в боте)            │
                            └─────────────────────┘
```

---

## 📝 Дополнительные материалы

- **[README.md](README.md)** — Краткое описание проекта
- **[PROJECT_HISTORY.md](PROJECT_HISTORY.md)** — Полная история разработки
- **[CLOUDPUB_SETUP.md](CLOUDPUB_SETUP.md)** — Детальная настройка CloudPub
- **[QUICKSTART_CLOUDPUB.txt](QUICKSTART_CLOUDPUB.txt)** — Краткая памятка CloudPub

### Документация модулей

- **[ai/README.md](ai/README.md)** — GigaChat API
- **[telethon/README.md](telethon/README.md)** — Сбор сообщений
- **[telebot/README.md](telebot/README.md)** — Telegram бот
- **[flask/README.md](flask/README.md)** — Flask Dashboard
- **[miniapp/README.md](miniapp/README.md)** — Telegram Mini App

---

## 🎯 Что дальше?

После успешного развертывания вы можете:

1. **Настроить автозапуск компонентов** при загрузке системы
2. **Добавить новые функции** (фильтры, теги, экспорт)
3. **Улучшить UI/UX** Flask и Mini App
4. **Настроить уведомления** о новых сообщениях
5. **Интегрировать другие AI модели** кроме GigaChat
6. **Добавить многопользовательский режим**
7. **Реализовать аналитику и отчеты**

---

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте логи в консоли каждого компонента
2. Запустите `python check_status.py`
3. Изучите [PROJECT_HISTORY.md](PROJECT_HISTORY.md) — там описаны все решенные проблемы
4. Проверьте, что все переменные в `.env` заполнены корректно

---

**Последнее обновление:** 10.12.2024  
**Версия:** 1.0.0  
**Автор:** AI-ассистент Cursor (Claude Sonnet 4.5)

