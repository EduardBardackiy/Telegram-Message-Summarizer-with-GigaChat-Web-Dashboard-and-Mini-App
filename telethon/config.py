"""Load Telegram client credentials from the project-level .env."""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Obtain your api_id and api_hash from https://my.telegram.org/apps
api_id: int = int(os.getenv("api_id") or 0)
api_hash: str = os.getenv("api_hash") or ""

# Telethon session name; a .session file will be created locally
session_name: str = os.getenv("session_name") or "tg_session"

# Bot username to monitor (optional, if empty - monitors all chats)
bot_username: str = os.getenv("MONITOR_BOT_USERNAME") or "@ED_Zerocoder_intensive_bot"
