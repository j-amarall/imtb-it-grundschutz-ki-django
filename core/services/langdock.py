import logging
from typing import Dict, List, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def validate_config() -> bool:
    return bool(
        getattr(settings, "LANGDOCK_API_KEY", "")
        and getattr(settings, "LANGDOCK_ASSISTANT_ID", "")
        and getattr(settings, "LANGDOCK_ASSISTANT_URL", "")
    )


def extract_assistant_text(data: Dict) -> str:
    """
    Erwartet Assistants Completions API:
    data["result"] ist eine Liste von Messages.
    assistant message: content ist häufig list[{text:"..."}] oder string.
    """
    result = data.get("result")
    if isinstance(result, list):
        for msg in reversed(result):
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                content = msg.get("content")

                if isinstance(content, list):
                    parts = []
                    for p in content:
                        if isinstance(p, dict) and isinstance(p.get("text"), str):
                            parts.append(p["text"])
                    return "\n".join(parts).strip()

                if isinstance(content, str):
                    return content.strip()

    return ""


def call_langdock_assistant(messages: List[Dict[str, str]]) -> Optional[str]:
    if not validate_config():
        logger.error("Langdock config missing")
        return None

    payload = {
        "assistantId": settings.LANGDOCK_ASSISTANT_ID,
        "messages": messages,
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {settings.LANGDOCK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            settings.LANGDOCK_ASSISTANT_URL,
            json=payload,
            headers=headers,
            timeout=getattr(settings, "LANGDOCK_TIMEOUT", 120),
        )
    except requests.RequestException:
        logger.exception("Langdock request failed")
        return None

    if resp.status_code != 200:
        logger.error("Langdock error %s: %s", resp.status_code, resp.text[:800])
        return None

    try:
        data = resp.json()
    except ValueError:
        logger.exception("Invalid JSON from Langdock")
        return None

    text = extract_assistant_text(data)
    return text or None
