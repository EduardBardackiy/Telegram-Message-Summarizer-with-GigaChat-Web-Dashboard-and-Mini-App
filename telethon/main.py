import asyncio
import logging
from datetime import timezone, timedelta
from typing import Optional

from telethon import TelegramClient, events
from telethon.errors import RPCError
from telethon.tl.types import Dialog

import config
from db import init_db, save_message

# Московский часовой пояс (UTC+3)
MSK = timezone(timedelta(hours=3))


# Configure logging for visibility into bot actions
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("tg-bot")


def ensure_config() -> None:
    """Sanity-check config values."""
    if not config.api_id or not config.api_hash or config.api_hash == "YOUR_API_HASH":
        raise RuntimeError(
            "Please set api_id and api_hash in config.py before running the bot."
        )


def build_client() -> TelegramClient:
    """Create and return a configured Telethon client."""
    return TelegramClient(
        config.session_name,
        config.api_id,
        config.api_hash,
        # Telethon will auto-reconnect; these parameters make it more robust
        request_retries=5,
        connection_retries=5,
        retry_delay=2,
    )


def format_sender(sender: Optional[object], chat_title: str) -> str:
    """
    Normalize sender display:
    - username
    - first/last name
    - title (for channels/chats)
    - fallback to chat title
    """
    if sender is None:
        return chat_title or "Unknown"

    username = getattr(sender, "username", None)
    if username:
        return username

    first_name = getattr(sender, "first_name", None)
    last_name = getattr(sender, "last_name", None)
    if first_name or last_name:
        return " ".join(filter(None, (first_name, last_name)))

    title = getattr(sender, "title", None)
    if title:
        return title

    return chat_title or "Unknown"


async def list_dialogs(client: TelegramClient) -> None:
    """Fetch and print available dialogs."""
    dialogs = await client.get_dialogs()
    logger.info("Available dialogs:")
    for idx, dialog in enumerate(dialogs, start=1):
        title = dialog.name or getattr(dialog.entity, "username", "Unknown")
        logger.info("  %d. %s (id=%s)", idx, title, dialog.id)


async def fetch_recent_messages(
    client: TelegramClient, dialog: Dialog, limit: int = 100
) -> None:
    """
    Fetch last `limit` messages from a dialog and store them in the database.
    """
    logger.info("Fetching last %d messages from chat id=%s", limit, dialog.id)
    chat_title = dialog.name or getattr(dialog.entity, "title", None) or "Unknown"
    async for message in client.iter_messages(dialog.entity, limit=limit):
        sender_entity = await message.get_sender()
        sender_label = format_sender(sender_entity, chat_title)

        message_data = {
            "id": message.id,
            "chat_id": dialog.id,
            "sender": sender_label,
            "text": message.message or "",
            "date": message.date.isoformat() if message.date else None,
        }
        save_message(message_data)
    logger.info("Finished fetching history for chat id=%s", dialog.id)


async def handle_new_message(event: events.NewMessage.Event) -> None:
    """
    Event handler for new incoming messages.
    Filter for specific bot if configured.
    """
    chat = await event.get_chat()
    chat_title = getattr(chat, "title", None) or getattr(chat, "username", "Unknown")
    chat_username = getattr(chat, "username", None)
    
    # Если настроен конкретный бот, фильтруем только его сообщения
    if config.bot_username:
        bot_username_clean = config.bot_username.lstrip("@")
        if chat_username != bot_username_clean:
            # Это не тот бот, пропускаем
            return
    
    sender_entity = await event.get_sender()
    sender = format_sender(sender_entity, chat_title)
    text = event.message.message or ""
    
    # Пропускаем сообщения от самого бота (ED_Zerocoder_intensive_bot)
    sender_username = getattr(sender_entity, "username", None)
    if sender_username and sender_username == "ED_Zerocoder_intensive_bot":
        # Это сообщение от нашего бота, не сохраняем
        return
    
    # Пропускаем служебные команды и кнопки
    if text.startswith("/") or text in ["📊 Статус", "📝 Саммаризация"]:
        # Это команда или нажатие кнопки, не сохраняем
        return

    # Конвертируем время в московское (UTC+3)
    message_date = None
    if event.message.date:
        message_date = event.message.date.astimezone(MSK).isoformat()
    
    message_data = {
        "id": event.message.id,
        "chat_id": event.chat_id,
        "sender": sender,
        "text": text,
        "date": message_date,
    }
    save_message(message_data)

    # Short log to console
    logger.info("[%s] %s: %s", chat_title, sender, text[:80])


async def choose_dialog(client: TelegramClient) -> Optional[Dialog]:
    """
    Utility to select the first dialog as an example.
    Replace this logic with user input if needed.
    """
    dialogs = await client.get_dialogs()
    if not dialogs:
        logger.warning("No dialogs available for this account.")
        return None
    return dialogs[0]


async def run_bot() -> None:
    """
    Main routine:
      - Initialize DB
      - Start Telethon client
      - List dialogs
      - Fetch recent messages from one dialog
      - Start live listener
    """
    ensure_config()
    init_db()

    client = build_client()

    # Robust start with reconnect handling
    while True:
        try:
            await client.start()
            break
        except RPCError as exc:
            logger.error("RPCError during start: %s. Retrying...", exc)
            await asyncio.sleep(3)

    await list_dialogs(client)

    # Register event handler for new messages from ALL dialogs
    client.add_event_handler(handle_new_message, events.NewMessage)
    logger.info("Listening for new messages from ALL chats... Press Ctrl+C to stop.")

    # Keep the client running
    try:
        await client.run_until_disconnected()
    except asyncio.CancelledError:
        logger.info("Shutdown requested, disconnecting...")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(run_bot())

