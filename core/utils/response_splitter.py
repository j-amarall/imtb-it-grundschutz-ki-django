import re
from typing import Tuple

# Heuristiken (DE): Start der Antwort
ANSWER_START_PATTERNS = [
    r"^\s*Kurzantwort\s*:",
    r"^\s*Antwort\s*:",
    r"^\s*Ergebnis\s*:",
    r"^\s*Zusammenfassung\s*:",
]

# Heuristiken (DE): Start des Hinweises/Disclaimers
HINT_START_PATTERNS = [
    r"^\s*Hinweis\s*:",
    r"^\s*Disclaimer\s*:",
    r"^\s*Wichtiger Hinweis\s*:",
]

# Wenn Reasoning oft mit "Assistent" oder englischen Bold-Headlines beginnt
REASONING_LIKELY_PATTERNS = [
    r"^\s*Assistent\b",
    r"^\s*\*\*.*\*\*\s*$",  # Markdown bold heading line
]

def split_reasoning_answer_hint(text: str) -> Tuple[str, str, str]:
    """
    Gibt (reasoning, answer, hint) zurück.
    - reasoning: alles vor "Kurzantwort:" (oder ähnlichen Markern)
    - answer: von "Kurzantwort:" bis vor "Hinweis:"
    - hint: ab "Hinweis:" bis Ende

    Wenn Marker fehlen, fallback:
    - alles als answer
    """
    if not text:
        return ("", "", "")

    lines = text.splitlines()

    # 1) finde Index wo Antwort startet
    answer_idx = None
    for i, line in enumerate(lines):
        for pat in ANSWER_START_PATTERNS:
            if re.search(pat, line, flags=re.IGNORECASE):
                answer_idx = i
                break
        if answer_idx is not None:
            break

    # Wenn keine "Kurzantwort" gefunden, dann keine sichere Trennung
    if answer_idx is None:
        # fallback: ggf. "Assistent" / englische headings als reasoning erkennen?
        # Wir bleiben konservativ: alles answer
        return ("", text.strip(), "")

    # reasoning ist alles davor (aber nur, wenn es plausibel aussieht)
    reasoning_block = "\n".join(lines[:answer_idx]).strip()
    answer_and_beyond = lines[answer_idx:]

    # 2) finde Hinweis-Start innerhalb des answer-Teils
    hint_idx_rel = None
    for j, line in enumerate(answer_and_beyond):
        for pat in HINT_START_PATTERNS:
            if re.search(pat, line, flags=re.IGNORECASE):
                hint_idx_rel = j
                break
        if hint_idx_rel is not None:
            break

    if hint_idx_rel is None:
        answer_block = "\n".join(answer_and_beyond).strip()
        hint_block = ""
    else:
        answer_block = "\n".join(answer_and_beyond[:hint_idx_rel]).strip()
        hint_block = "\n".join(answer_and_beyond[hint_idx_rel:]).strip()

    # Wenn reasoning leer ist oder nur Müll, leeren wir es
    if reasoning_block:
        # Plausibilitätscheck: wenn es komplett deutsch ist und wie echte Antwort klingt,
        # könnte es sein, dass das Modell keine reasoning geliefert hat.
        # Wir halten es simpel: reasoning nur anzeigen wenn es sehr "reasoning-typisch" ist.
        if not any(re.search(p, reasoning_block, flags=re.IGNORECASE | re.MULTILINE) for p in REASONING_LIKELY_PATTERNS):
            # Trotzdem kann reasoning da sein; aber du willst "Gedanken" explizit sehen.
            # Wir lassen es stehen — du kannst es im UI einklappbar machen.
            pass

    return (reasoning_block, answer_block, hint_block)
