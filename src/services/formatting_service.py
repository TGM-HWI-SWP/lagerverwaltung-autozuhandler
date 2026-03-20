from __future__ import annotations

from domain.enums import InvoiceStatus, PartStatus

SPECIAL_WORDS = {
    "bmw": "BMW",
    "vw": "VW",
    "audi": "Audi",
    "mercedes": "Mercedes",
    "skoda": "Skoda",
    "toyota": "Toyota",
    "ford": "Ford",
    "tesla": "Tesla",
    "öl": "Öl",
    "abs": "ABS",
    "led": "LED",
    "xenon": "Xenon",
    "suv": "SUV",
    "gti": "GTI",
    "porsche": "Porsche",
    "opel": "Opel",
}


def safe_str(value: object | None) -> str:
    return "" if value is None else str(value).strip()


def smart_capitalize(text: object | None) -> str:
    if text is None:
        return ""

    value = str(text).strip()
    if not value:
        return ""

    words = value.split()
    result: list[str] = []

    for word in words:
        lower_word = word.lower()

        if lower_word in SPECIAL_WORDS:
            result.append(SPECIAL_WORDS[lower_word])
            continue

        if "-" in word:
            dash_parts: list[str] = []
            for part in word.split("-"):
                lower_part = part.lower()
                if lower_part in SPECIAL_WORDS:
                    dash_parts.append(SPECIAL_WORDS[lower_part])
                else:
                    dash_parts.append(part[:1].upper() + part[1:].lower() if part else "")
            result.append("-".join(dash_parts))
            continue

        result.append(word[:1].upper() + word[1:].lower())

    return " ".join(result)


def format_currency(value: object) -> str:
    try:
        return f"{float(value):.2f} €"
    except (TypeError, ValueError):
        return "0.00 €"


def normalize_db_list(values: list[object]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        normalized = safe_str(value)
        if normalized and normalized.lower() not in seen:
            seen.add(normalized.lower())
            result.append(normalized)

    result.sort(key=lambda x: x.lower())
    return result


def part_status_badge(status: str | PartStatus) -> str:
    value = status.value if isinstance(status, PartStatus) else status
    mapping = {
        PartStatus.AVAILABLE.value: "🟢 Verfügbar",
        PartStatus.REORDER.value: "🟡 Nachbestellen",
        PartStatus.UNAVAILABLE.value: "🔴 Nicht verfügbar",
    }
    return mapping.get(value, value)


def invoice_status_badge(status: str | InvoiceStatus) -> str:
    value = status.value if isinstance(status, InvoiceStatus) else status
    mapping = {
        InvoiceStatus.OPEN.value: "🟠 Offen",
        InvoiceStatus.PAID.value: "🟢 Bezahlt",
        InvoiceStatus.CANCELED.value: "🔴 Storniert",
    }
    return mapping.get(value, value)