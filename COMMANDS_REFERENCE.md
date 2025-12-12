# 📝 Справочник команд и скриптов TGBot проекта

Быстрый справочник всех доступных команд, скриптов и инструментов проекта.

---

## 🚀 Запуск компонентов

### Активация виртуального окружения
```powershell
.\.venv\Scripts\Activate.ps1
```

### Telethon (сбор сообщений из Telegram)
```powershell
python telethon\main.py
```
**Назначение:** Слушает сообщения в Telegram и сохраняет их в БД  
**Порт:** —  
**Требует:** API_ID, API_HASH в .env

### Summary Bot (Telegram бот)
```powershell
python telebot\summary_bot.py
```
**Назначение:** Telegram бот для саммаризации по команде  
**Порт:** —  
**Требует:** BOT_TOKEN, GIGACHAT credentials в .env  
**Команды бота:** 📊 Статус, 📝 Саммаризация

### Flask Dashboard (веб-интерфейс)
```powershell
python flask\app.py
```
**Назначение:** Веб-дашборд для мониторинга  
**Порт:** 5000  
**URL:** http://localhost:5000  
**Функции:** Просмотр статистики, списка сообщений, управление

### Telegram Mini App
```powershell
python miniapp\app.py
```
**Назначение:** Mini App для Telegram  
**Порт:** 5001  
**URL:** http://localhost:5001  
**Функции:** То же что Flask, но оптимизировано для Telegram

---

## 🌐 CloudPub туннели

### Автоматический запуск (PowerShell)
```powershell
.\start_tunnels.ps1
```
**Назначение:** Автоматическая регистрация и запуск туннелей  
**Результат:** 2 публичных URL (для Flask и Mini App)

### Автоматический запуск (Python)
```powershell
python start_tunnels.py
```
**Назначение:** То же что и PowerShell скрипт, но через Python  
**Преимущества:** Кроссплатформенность, красивый вывод

### Ручной запуск туннелей
```powershell
# Авторизация (один раз)
clo login

# Вариант 1: Регистрация и запуск всех туннелей вместе
clo register http 5000
clo register http 5001
clo run

# Вариант 2: Публикация (регистрация + запуск) каждого туннеля отдельно
clo publish http 5000    # Терминал 1
clo publish http 5001    # Терминал 2
```

### Управление туннелями
```powershell
# Опции конфигурации CloudPub
clo options

# Список зарегистрированных сервисов
clo ls

# Удаление сервиса
clo unpublish http 5000
clo unpublish http 5001

# Очистка всех регистраций
clo clean

# Остановка публикации
clo stop

# Проверка подключения к серверу
clo ping

# Выход (удаление токена)
clo logout
```

---

## 🔍 Диагностика и проверка

### Проверка статуса всех компонентов
```powershell
python check_status.py
```
**Назначение:** Комплексная проверка состояния системы  
**Проверяет:**
- Запущенные сервисы (Flask, Mini App)
- Базу данных (количество сообщений)
- CloudPub (установка, авторизация)
- Конфигурацию (.env файл)
- Структуру проекта

### Проверка базы данных

**Общее количество сообщений:**
```powershell
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM messages'); print('Всего сообщений:', cursor.fetchone()[0]); conn.close()"
```

**Необработанные сообщения:**
```powershell
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM messages WHERE summarized = 0'); print('Необработанных:', cursor.fetchone()[0]); conn.close()"
```

**Обработанные сообщения:**
```powershell
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM messages WHERE summarized = 1'); print('Обработанных:', cursor.fetchone()[0]); conn.close()"
```

**Последнее сообщение:**
```powershell
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('SELECT text, timestamp FROM messages ORDER BY id DESC LIMIT 1'); msg = cursor.fetchone(); print(f'Текст: {msg[0]}\nВремя: {msg[1]}') if msg else print('Нет сообщений'); conn.close()"
```

---

## 🛠️ Управление GigaChat

### Обновление токена доступа
```powershell
python scripts/update_token.py
```
**Назначение:** Получение нового access token от GigaChat API  
**Когда использовать:** Если GigaChat перестал отвечать

### Проверка подключения к GigaChat
```powershell
python ai\main.py
```
**Назначение:** CLI для тестирования саммаризации  
**Интерактивный режим:** Введите текст для саммаризации

---

## 🔧 Управление процессами

### Остановка всех Python процессов
```powershell
taskkill /F /IM python.exe
```
**⚠️ Осторожно:** Остановит ВСЕ Python процессы в системе

### Поиск Python процессов
```powershell
Get-Process python
```

### Остановка конкретного процесса
```powershell
Stop-Process -Id <PID> -Force
```

---

## 🗃️ Управление базой данных

### Очистка базы данных (удаление всех сообщений)
```powershell
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('DELETE FROM messages'); conn.commit(); print(f'Удалено сообщений: {cursor.rowcount}'); conn.close()"
```

### Сброс флага обработки (все сообщения → необработанные)
```powershell
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('UPDATE messages SET summarized = 0'); conn.commit(); print(f'Обновлено: {cursor.rowcount}'); conn.close()"
```

### Создание бэкапа БД
```powershell
copy messages.db messages_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db
```

### Восстановление из бэкапа
```powershell
copy messages_backup_YYYYMMDD_HHMMSS.db messages.db
```

---

## 📞 Telegram Bot API

### Проверка информации о webhook
```powershell
Invoke-WebRequest -Uri "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getWebhookInfo"
```

### Удаление webhook
```powershell
Invoke-WebRequest -Uri "https://api.telegram.org/bot<ВАШ_ТОКЕН>/deleteWebhook?drop_pending_updates=true"
```

### Получение информации о боте
```powershell
Invoke-WebRequest -Uri "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getMe"
```

### Получение обновлений (последние сообщения)
```powershell
Invoke-WebRequest -Uri "https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"
```

---

## 📦 Управление зависимостями

### Установка всех зависимостей
```powershell
pip install -r requirements.txt
```

### Обновление зависимостей
```powershell
pip install --upgrade -r requirements.txt
```

### Экспорт текущих зависимостей
```powershell
pip freeze > requirements_current.txt
```

### Проверка устаревших пакетов
```powershell
pip list --outdated
```

---

## 🎨 Разработка

### Создание новой миграции БД
```powershell
python -c "import sqlite3; # добавьте код миграции"
```

### Тестирование GigaChat интеграции
```powershell
python ai\gigachat.py
```

### Тестирование Telethon подключения
```powershell
python telethon\config.py
```

---

## 📊 Логи и мониторинг

### Просмотр логов Flask
```powershell
# Flask выводит логи в консоль при запуске
python flask\app.py
```

### Просмотр логов Telethon
```powershell
# Telethon выводит логи в консоль при запуске
python telethon\main.py
```

### Просмотр логов CloudPub
```powershell
clo logs
```

---

## 🧹 Очистка и обслуживание

### Очистка кэша Python
```powershell
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
```

### Удаление виртуального окружения
```powershell
Remove-Item -Recurse -Force .venv
```

### Пересоздание виртуального окружения
```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🔐 Безопасность

### Проверка .env файла
```powershell
Get-Content .env
```

### Скрытие конфиденциальных данных в логах
```powershell
# Все скрипты уже настроены на скрытие токенов в логах
```

### Проверка прав доступа к файлам
```powershell
Get-Acl messages.db | Format-List
```

---

## 📚 Документация

### Открытие основной документации
```powershell
# В браузере откройте:
README.md                    # Краткое описание
PROJECT_HISTORY.md          # История разработки
DEPLOYMENT_GUIDE.md         # Полное руководство по развертыванию
CLOUDPUB_SETUP.md           # Настройка CloudPub
QUICKSTART_CLOUDPUB.txt     # Краткая памятка CloudPub
COMMANDS_REFERENCE.md       # Этот файл
```

### Документация модулей
```powershell
ai\README.md                # GigaChat API
telethon\README.md          # Telethon
telebot\README.md           # Telegram Bot
flask\README.md             # Flask Dashboard
miniapp\README.md           # Telegram Mini App
```

---

## 🔗 Полезные URL

### Локальные
- Flask Dashboard: http://localhost:5000
- Telegram Mini App: http://localhost:5001

### Внешние сервисы
- GigaChat: https://developers.sber.ru/
- CloudPub: https://cloudpub.ru
- Telegram Bot API: https://core.telegram.org/bots/api
- Telegram My Apps: https://my.telegram.org/apps
- BotFather: https://t.me/BotFather

---

## 💡 Быстрые рецепты

### Полный перезапуск системы
```powershell
# 1. Остановить все процессы
taskkill /F /IM python.exe

# 2. Активировать окружение
.\.venv\Scripts\Activate.ps1

# 3. Запустить компоненты (в разных терминалах)
python telethon\main.py
python telebot\summary_bot.py
python flask\app.py
python miniapp\app.py

# 4. Запустить туннели
.\start_tunnels.ps1
```

### Быстрая диагностика проблем
```powershell
# Проверить статус системы
python check_status.py

# Проверить БД
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM messages WHERE summarized = 0'); print('Необработанных:', cursor.fetchone()[0]); conn.close()"

# Проверить CloudPub
clo options

# Проверить порты
Test-NetConnection -ComputerName localhost -Port 5000
Test-NetConnection -ComputerName localhost -Port 5001
```

### Сброс и свежий старт
```powershell
# 1. Остановить все
taskkill /F /IM python.exe

# 2. Создать бэкап БД
copy messages.db messages_backup.db

# 3. Очистить БД
python -c "import sqlite3; conn = sqlite3.connect('messages.db'); cursor = conn.cursor(); cursor.execute('DELETE FROM messages'); conn.commit(); conn.close()"

# 4. Удалить webhook
Invoke-WebRequest -Uri "https://api.telegram.org/bot<ТОКЕН>/deleteWebhook?drop_pending_updates=true"

# 5. Запустить заново
.\.venv\Scripts\Activate.ps1
python telethon\main.py
python telebot\summary_bot.py
```

---

## 🎯 Часто используемые комбинации

### Развертывание с нуля
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy env.example .env
# Отредактируйте .env
python telethon\main.py  # Авторизация Telethon
```

### Ежедневный запуск
```powershell
.\.venv\Scripts\Activate.ps1
python check_status.py
# Запустите недостающие компоненты
```

### Публикация Mini App
```powershell
# В терминале 1
python miniapp\app.py

# В терминале 2
.\start_tunnels.ps1

# Скопируйте URL для порта 5001 и настройте в @BotFather
```

---

**Последнее обновление:** 10.12.2024  
**Версия:** 1.0.0

Для получения дополнительной помощи см. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

