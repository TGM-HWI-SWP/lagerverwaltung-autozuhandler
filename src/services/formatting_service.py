from __future__ import annotations
 
 
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
 
 
def safe_str(value: object) -> str:
    return "" if value is None else str(value).strip()
 
 
def smart_capitalize(text: object) -> str:
    if text is None:
        return ""
 
    text = str(text).strip()
    if not text:
        return ""
 
    words = text.split()
    result: list[str] = []
 
    for word in words:
        lower_word = word.lower()
        if lower_word in SPECIAL_WORDS:
            result.append(SPECIAL_WORDS[lower_word])
        elif "-" in word:
            parts_dash: list[str] = []
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
 
 
def format_currency(value: object) -> str:
    try:
        return f"{float(value):.2f} €"
    except Exception:
        return "0.00 €"
 
 
def calc_profit(purchase_price: object, sale_price: object) -> float:
    try:
        return float(sale_price) - float(purchase_price)
    except Exception:
        return 0.0
 
 
def invoice_status_badge(status: str) -> str:
    mapping = {
        "Offen": "🟠 Offen",
        "Bezahlt": "🟢 Bezahlt",
        "Storniert": "🔴 Storniert",
    }
    return mapping.get(status, status)
 
 
def part_status_badge(status: str) -> str:
    mapping = {
        "Verfügbar": "🟢 Verfügbar",
        "Nachbestellen": "🟡 Nachbestellen",
        "Nicht verfügbar": "🔴 Nicht verfügbar",
    }
    return mapping.get(status, status)