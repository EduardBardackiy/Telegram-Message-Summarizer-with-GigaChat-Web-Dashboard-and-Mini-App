import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path("messages.db")


def init_db() -> None:
    """
    Initialize the SQLite database and ensure the messages table exists.
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                sender TEXT,
                text TEXT,
                date TEXT,
                summarized INTEGER DEFAULT 0
            )
            """
        )
        # Добавляем колонку summarized, если её нет (для существующих БД)
        try:
            conn.execute("ALTER TABLE messages ADD COLUMN summarized INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # колонка уже существует
        conn.commit()


def save_message(message_data: Dict[str, Any]) -> None:
    """
    Persist a message to the database if it is not already stored.

    message_data expects keys: id, chat_id, sender, text, date
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        # Avoid duplicates via INSERT OR IGNORE on the primary key
        conn.execute(
            """
            INSERT OR IGNORE INTO messages (id, chat_id, sender, text, date, summarized)
            VALUES (:id, :chat_id, :sender, :text, :date, 0)
            """,
            message_data,
        )
        conn.commit()


def get_unsummarized_messages(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Получить несаммаризованные сообщения из БД.
    Возвращает список словарей с ключами: id, chat_id, sender, text, date.
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            """
            SELECT id, chat_id, sender, text, date
            FROM messages
            WHERE summarized = 0 AND text IS NOT NULL AND text != ''
            ORDER BY date ASC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]


def mark_as_summarized(message_id: int) -> None:
    """
    Пометить сообщение как саммаризованное.
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "UPDATE messages SET summarized = 1 WHERE id = ?",
            (message_id,),
        )
        conn.commit()


def save_summary(message_id: int, summary_text: str) -> None:
    """
    Сохранить саммаризацию в отдельную запись (как ответ бота).
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        # Генерируем уникальный ID для саммаризации
        summary_id = message_id * 10_000 + 9999
        conn.execute(
            """
            INSERT OR REPLACE INTO messages (id, chat_id, sender, text, date, summarized)
            VALUES (?, (SELECT chat_id FROM messages WHERE id = ?), 'bot_summary', ?, datetime('now'), 1)
            """,
            (summary_id, message_id, summary_text),
        )
        conn.commit()

