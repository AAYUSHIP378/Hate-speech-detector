
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


def detect_language(text: str):

    text = text.strip()

    if len(text) < 3:
        return "Unknown"

    try:
        lang = detect(text)
    except:
        lang = "unknown"

    if lang == "hi":
        return "Hindi"
    elif lang == "en":
        return "English"
    else:
        return "Hinglish / Mixed"


def rule_based_hate(text: str):

    hate_words = [
        "kill",
        "terrorist",
        "rapist",
        "dirty",
        "slave",
        "hate",
        "bloody",
        "pig",
        "maar dungi"
    ]

    text = text.lower()

    for w in hate_words:
        if w in text:
            return True

    return False