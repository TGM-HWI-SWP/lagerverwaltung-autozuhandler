from src.domain.enums import SPECIAL_WORDS


def smart_capitalize(text) -> str:
    if text is None:
        return ""
    text = str(text).strip()
    if not text:
        return ""

    words = text.split()
    result = []

    for word in words:
        lower_word = word.lower()
        if lower_word in SPECIAL_WORDS:
            result.append(SPECIAL_WORDS[lower_word])
        elif "-" in word:
            parts_dash = []
            for part in word.split("-"):
                p = part.lower()
                if p in SPECIAL_WORDS:
                    parts_dash.append(SPECIAL_WORDS[p])
                else:
                    parts_dash.append(part[:1].upper() + part[1:].lower() if part else "")
            result.append("-".join(parts_dash))
        else:
            result.append(word[:1].upper() + word[1:].lower())

    return " ".join(result)


def safe_str(value) -> str:
    return "" if value is None else str(value).strip()


def format_currency(value) -> str:
    try:
        return f"{float(value):.2f} €"
    except Exception:
        return "0.00 €"


def part_status_badge(status: str) -> str:
    mapping = {
        "Verfügbar": "🟢 Verfügbar",
        "Nachbestellen": "🟡 Nachbestellen",
        "Nicht verfügbar": "🔴 Nicht verfügbar",
    }
    return mapping.get(status, status)


def invoice_status_badge(status: str) -> str:
    mapping = {
        "Offen": "🟠 Offen",
        "Bezahlt": "🟢 Bezahlt",
        "Storniert": "🔴 Storniert",
    }
    return mapping.get(status, status)


def calc_profit(purchase_price, sale_price) -> float:
    try:
        return float(sale_price) - float(purchase_price)
    except Exception:
        return 0.0


def normalize_db_list(values):
    seen = set()
    result = []
    for v in values:
        val = str(v).strip()
        if val and val.lower() not in seen:
            seen.add(val.lower())
            result.append(val)
    result.sort(key=lambda x: x.lower())
    return result