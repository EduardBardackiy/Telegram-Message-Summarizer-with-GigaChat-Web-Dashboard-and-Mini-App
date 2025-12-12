# GigaChat Summary CLI

Простой CLI на Python для получения краткого саммари текста через GigaChat API.

## Стек
- Python 3.10+
- requests
- argparse
- python-dotenv

## Структура
- `main.py` — CLI-приложение (`summary` команда для создания саммари).
- `gigachat.py` — запросы к GigaChat (OAuth и chat/completions).
- `utils.py` — утилиты (env, чтение файлов).
- `.env` — хранит `CLIENT_ID`, `CLIENT_SECRET`.

## Установка
1) Создайте и активируйте виртуальное окружение (рекомендуется):
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
2) Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка .env
Используется `.env` в корне проекта. Пример см. `env.example`.
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

## Использование
Из каталога `ai/`:
```bash
python main.py summary --file messages.txt
# или
python main.py summary --text "Ваш текст для саммаризации"
```
Приоритет входных данных: `--text` > `--file`. Если не указать ни один аргумент — будет выведена ошибка и справка.

## Пример ответа
Вывод в консоль:
```
--- Summary ---

<краткое саммари>

--------------
```

## Обработка ошибок
- Ошибки чтения файла или отсутствия аргументов выводятся в stderr.
- Ошибки GigaChat (OAuth или completions) выводятся с текстом ответа.
- Непредвидённые ошибки логируются.

