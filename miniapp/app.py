"""
Telegram Mini App для мониторинга системы саммаризации.
Работает внутри Telegram через Web Apps API.
"""
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Путь к базе данных (на уровень выше)
DB_PATH = Path(__file__).parent.parent / "messages.db"


def get_db_connection():
    """Создать подключение к БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_statistics():
    """Получить статистику из БД."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Всего сообщений
    cursor.execute("SELECT COUNT(*) as total FROM messages")
    total = cursor.fetchone()["total"]
    
    # Проанализировано
    cursor.execute("SELECT COUNT(*) as analyzed FROM messages WHERE summarized = 1")
    analyzed = cursor.fetchone()["analyzed"]
    
    # Необработанных
    unsummarized = total - analyzed
    
    # Последняя саммаризация
    cursor.execute("""
        SELECT MAX(date) as last_summary 
        FROM messages 
        WHERE summarized = 1
    """)
    result = cursor.fetchone()
    last_summary = result["last_summary"] if result["last_summary"] else "Нет данных"
    
    conn.close()
    
    return {
        "total": total,
        "analyzed": analyzed,
        "unsummarized": unsummarized,
        "last_summary": last_summary,
        "percentage": round((analyzed / total * 100) if total > 0 else 0, 1)
    }


def get_all_messages(limit=50, offset=0):
    """Получить все сообщения с пагинацией."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, chat_id, sender, text, date, summarized
        FROM messages
        ORDER BY date DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))
    
    messages = [dict(row) for row in cursor.fetchall()]
    
    # Получаем общее количество
    cursor.execute("SELECT COUNT(*) as total FROM messages")
    total = cursor.fetchone()["total"]
    
    conn.close()
    
    return messages, total


@app.route("/")
def index():
    """Главная страница - дашборд."""
    stats = get_statistics()
    return render_template("index.html", stats=stats)


@app.route("/messages")
def messages():
    """Страница со списком сообщений."""
    page = int(request.args.get("page", 1))
    per_page = 30
    offset = (page - 1) * per_page
    
    messages_list, total = get_all_messages(limit=per_page, offset=offset)
    total_pages = (total + per_page - 1) // per_page
    
    return render_template(
        "messages.html",
        messages=messages_list,
        page=page,
        total_pages=total_pages,
        total=total
    )


@app.route("/api/stats")
def api_stats():
    """API endpoint для получения статистики."""
    stats = get_statistics()
    return jsonify(stats)


@app.template_filter("format_datetime")
def format_datetime(value):
    """Форматирование даты и времени."""
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return value


@app.template_filter("truncate_text")
def truncate_text(text, length=60):
    """Обрезать текст до указанной длины."""
    if not text:
        return ""
    if len(text) <= length:
        return text
    return text[:length] + "..."


if __name__ == "__main__":
    print(f"🚀 Telegram Mini App запущен")
    print(f"📊 База данных: {DB_PATH}")
    print(f"✅ Существует: {DB_PATH.exists()}")
    app.run(debug=True, host="0.0.0.0", port=5001)

