import logging
import os
import uuid
from typing import Any, Dict

import requests

from utils import encode_basic_auth

logger = logging.getLogger("gigachat.api")


class GigaChatError(Exception):
    """Base exception for GigaChat API issues."""


def _get_verify_flag() -> bool | str:
    """
    Resolve SSL verification setting.
    - If GIGACHAT_CA_BUNDLE is set: pass path to requests.verify.
    - Else use GIGACHAT_VERIFY (true/false). Defaults to True.
    """
    ca_bundle = os.getenv("GIGACHAT_CA_BUNDLE")
    if ca_bundle:
        return ca_bundle

    verify_env = os.getenv("GIGACHAT_VERIFY")
    if verify_env is None:
        return True
    return verify_env.lower() in {"1", "true", "yes", "y"}


def get_access_token() -> str:
    """
    Obtain OAuth access token using CLIENT_ID and CLIENT_SECRET from env.
    """
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if not client_id or not client_secret:
        raise GigaChatError("CLIENT_ID или CLIENT_SECRET не заданы в .env")

    # Official OAuth endpoint
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_basic_auth(client_id, client_secret)}",
        "RqUID": str(uuid.uuid4()),
    }
    scope = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    payload = {"scope": scope}

    logger.info("Запрашиваем OAuth токен")
    verify = _get_verify_flag()
    resp = requests.post(url, data=payload, headers=headers, timeout=30, verify=verify)
    if resp.status_code != 200:
        raise GigaChatError(f"OAuth error {resp.status_code}: {resp.text}")

    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise GigaChatError("Не удалось получить access_token из ответа OAuth")
    return token


def generate_summary(text: str) -> str:
    """
    Send text to GigaChat chat/completions and return summary.
    """
    token = get_access_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload: Dict[str, Any] = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": "Ты – ассистент, который делает краткие выжимки текста.",
            },
            {"role": "user", "content": text},
        ],
    }

    logger.info("Отправляем текст в GigaChat на саммаризацию")
    verify = _get_verify_flag()
    resp = requests.post(url, json=payload, headers=headers, timeout=60, verify=verify)
    if resp.status_code != 200:
        raise GigaChatError(f"GigaChat error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise GigaChatError(f"Непредвиденный формат ответа: {data}") from exc


def ask_gigachat(
    user_text: str,
    system_prompt: str = "Ты — дружелюбный ассистент. Отвечай кратко и по делу.",
) -> str:
    """
    Отправить произвольный запрос в GigaChat и вернуть ответ.
    """
    token = get_access_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload: Dict[str, Any] = {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
    }

    logger.info("Отправляем произвольный запрос в GigaChat")
    verify = _get_verify_flag()
    resp = requests.post(url, json=payload, headers=headers, timeout=60, verify=verify)
    if resp.status_code != 200:
        raise GigaChatError(f"GigaChat error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise GigaChatError(f"Непредвиденный формат ответа: {data}") from exc

