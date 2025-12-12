import base64
import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger("gigachat.utils")


def init_env(env_path: str | None = None) -> None:
    """Load environment variables from .env at project root by default."""
    default_path = Path(__file__).resolve().parent.parent / ".env"
    path = env_path or default_path
    load_dotenv(path)
    logger.debug("Environment variables loaded from %s", path)


def encode_basic_auth(client_id: str, client_secret: str) -> str:
    """Return HTTP Basic token for client credentials."""
    token = f"{client_id}:{client_secret}".encode("utf-8")
    return base64.b64encode(token).decode("utf-8")


def read_text_from_file(path: str) -> str:
    """Read text content from a file."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return file_path.read_text(encoding="utf-8")


def pick_input_text(text_arg: Optional[str], file_arg: Optional[str]) -> str:
    """
    Choose input text: priority to direct text, otherwise from file.
    Raises ValueError if neither provided.
    """
    if text_arg:
        return text_arg
    if file_arg:
        return read_text_from_file(file_arg)
    raise ValueError("Не передан текст: используйте --text или --file")

