# Telegram Bot on Telethon

Асинхронный скрипт на Python, использующий Telethon для:
- Подключения к Telegram по API ключам.
- Получения списка диалогов.
- Выгрузки последних N сообщений выбранного чата.
- Live-обработки новых сообщений с сохранением в SQLite и коротким логом.

## Структура
- `main.py` — точка входа, логика клиента, сбор истории, live-listener.
- `db.py` — инициализация и запись в SQLite (`messages.db`), защита от дублей.
- `config.py` — конфигурация `api_id`, `api_hash`, `session_name`.
- `requirements.txt` — зависимости.

## Настройка
1) Установите Python 3.10+.
2) (Рекомендуется) создать виртуальное окружение:
   - Windows (PowerShell):
     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3) Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4) Заполните `.env` в корне проекта (см. `env.example`):
   ```
   api_id=123456
   api_hash=YOUR_API_HASH
   session_name=tg_session
   ```
   Ключи берутся на https://my.telegram.org/apps.

## Запуск
Находясь в каталоге `telethon/`:
```bash
python main.py
```
Или из корня проекта:
```bash
python telethon/main.py
```
Поведение:
- При старте выводит список доступных диалогов.
- Собирает последние 100 сообщений из первого диалога (логику выбора можно изменить в `choose_dialog()`).
- Запускает live-слушатель новых сообщений и сохраняет их в `messages.db`.
- Логи в консоли в формате `[CHAT TITLE] sender: text`.

## Полезно знать
- Сессия сохраняется в файл `<session_name>.session` рядом с проектом.
- База `messages.db` создаётся автоматически.
- Повторный запуск безопасен: записи защищены от дублей по `id` сообщения.

