"""
Telegram-бот для саммаризации сообщений по команде.
Работает с БД, которую наполняет Telethon.
"""
import logging
import os
import sys
from pathlib import Path

import telebot
from telebot import types
from dotenv import load_dotenv

# Загружаем переменные окружения
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Подключаем модули
sys.path.insert(0, str(ROOT_DIR / "ai"))
sys.path.insert(0, str(ROOT_DIR / "telethon"))

from gigachat import GigaChatError, generate_summary  # noqa: E402
from db import (  # noqa: E402
    init_db,
    get_unsummarized_messages,
    mark_as_summarized,
    save_summary,
)

# Получаем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле")

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("summary_bot")


def get_main_keyboard():
    """Создать главную клавиатуру с кнопками."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_status = types.KeyboardButton("📊 Статус")
    btn_summary = types.KeyboardButton("📝 Саммаризация")
    keyboard.add(btn_status, btn_summary)
    return keyboard


@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    """Приветствие и подсказка."""
    help_text = """
👋 Привет! Я бот для саммаризации сообщений.

Используйте кнопки ниже:
📊 Статус - количество необработанных сообщений
📝 Саммаризация - получить выжимку новых сообщений

Или команды: /status, /summary
"""
    bot.reply_to(message, help_text, reply_markup=get_main_keyboard())


@bot.message_handler(commands=["status"])
def handle_status(message):
    """Показать статистику."""
    messages = get_unsummarized_messages(limit=1000)
    count = len(messages)
    bot.reply_to(message, f"📊 Необработанных сообщений: {count}", reply_markup=get_main_keyboard())


@bot.message_handler(commands=["summary"])
def handle_summary(message):
    """Создать саммаризацию всех новых сообщений."""
    logger.info("Запрос на саммаризацию от %s", message.from_user.username or message.from_user.id)
    
    bot.send_chat_action(message.chat.id, "typing")
    
    try:
        # Получаем все несаммаризованные сообщения
        messages = get_unsummarized_messages(limit=100)
        
        if not messages:
            bot.reply_to(message, "✅ Нет новых сообщений для саммаризации.", reply_markup=get_main_keyboard())
            return
        
        # Фильтруем короткие сообщения
        valid_messages = [msg for msg in messages if msg.get("text") and len(msg["text"].strip()) >= 10]
        
        if not valid_messages:
            bot.reply_to(
                message, 
                f"Найдено {len(messages)} сообщений, но все слишком короткие (< 10 символов).",
                reply_markup=get_main_keyboard()
            )
            # Помечаем короткие как обработанные
            for msg in messages:
                mark_as_summarized(msg["id"])
            return
        
        # Объединяем тексты сообщений
        combined_text = "\n\n---\n\n".join([
            f"От {msg['sender']} ({msg['date']}):\n{msg['text']}"
            for msg in valid_messages
        ])
        
        logger.info("Саммаризация %d сообщений (общая длина: %d символов)", 
                   len(valid_messages), len(combined_text))
        
        bot.reply_to(message, f"⏳ Обрабатываю {len(valid_messages)} сообщений...")
        
        # Создаём саммаризацию через GigaChat
        summary = generate_summary(combined_text)
        
        # Сохраняем саммаризацию для первого сообщения (как общую)
        save_summary(valid_messages[0]["id"], summary)
        
        # Помечаем все сообщения как обработанные
        for msg in messages:
            mark_as_summarized(msg["id"])
        
        # Отправляем результат
        response = f"📝 Выжимка из {len(valid_messages)} сообщений:\n\n{summary}"
        bot.reply_to(message, response, reply_markup=get_main_keyboard())
        
        logger.info("✓ Саммаризация отправлена пользователю")
        
    except GigaChatError as err:
        logger.error("GigaChat error: %s", err)
        bot.reply_to(message, "❌ Ошибка GigaChat. Попробуйте позже.", reply_markup=get_main_keyboard())
    except Exception as err:  # pragma: no cover
        logger.exception("Unexpected error: %s", err)
        bot.reply_to(message, "❌ Не удалось создать саммаризацию.", reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda message: message.text == "📊 Статус")
def handle_status_button(message):
    """Обработчик кнопки Статус."""
    handle_status(message)


@bot.message_handler(func=lambda message: message.text == "📝 Саммаризация")
def handle_summary_button(message):
    """Обработчик кнопки Саммаризация."""
    handle_summary(message)


def main():
    """Запуск бота."""
    logger.info("Запуск бота саммаризации по команде...")
    init_db()
    
    try:
        # Снимаем webhook
        try:
            bot.remove_webhook()
        except Exception as err:
            logger.warning("Не удалось снять webhook: %s", err)
        
        bot.infinity_polling(none_stop=True)
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
    except Exception as err:  # pragma: no cover
        logger.error("Ошибка при работе бота: %s", err)
        raise


if __name__ == "__main__":
    main()

