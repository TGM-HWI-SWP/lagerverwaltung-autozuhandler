from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd

# =========================================================
# Konfiguration
# =========================================================
APP_TITLE = "Autozuhändler"
NEXTCLOUD_EXPORT_DIR = Path(r"C:\Nextcloud_Autozu\exports")
NEXTCLOUD_EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Demo-Mitarbeiter-Login
# In einer echten produktiven App bitte Passwörter hashen und nicht im Code speichern.
EMPLOYEES = {
    "Julian": {"password": "admin123", "role": "admin", "name": "Julian"},
    "Fabienne": {"password": "admin456", "role": "admin", "name": "Fabienne"},
    "Mikail": {"password": "admin789", "role": "admin", "name": "Miki"},
    "Sirin": {"password": "admin000", "role": "admin", "name": "Sirin"},
    "verkauf": {"password": "verkauf123", "role": "Mitarbeiter", "name": "Max Verkauf"},
    "lager": {"password": "lager123", "role": "Mitarbeiter", "name": "Lena Lager"},
    "lehrer": {"password": "lehrer123", "role": "Lehrer", "name": "Schobi Ratschi"},
}

cars: list[dict] = []
parts: list[dict] = []
customers: list[dict] = []

brand_db = ["Audi", "BMW", "Mercedes", "VW", "Skoda", "Toyota", "Ford", "Tesla"]
category_db = ["Reifen", "Felgen", "Bremsen", "Öl", "Batterie", "Licht", "Innenraum", "Zubehör"]

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
}

CAR_STATUSES = ["Verfügbar", "Reserviert", "Verkauft"]
PART_STATUSES = ["Verfügbar", "Nachbestellen", "Nicht verfügbar"]
INVOICE_STATUSES = ["Offen", "Bezahlt", "Storniert"]
FUELS = ["Benzin", "Diesel", "Hybrid", "Elektro"]


# =========================================================
# Formatierung / IDs
# =========================================================
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


def generate_next_id(prefix: str, existing_ids: list[str]) -> str:
    numbers = []
    for item_id in existing_ids:
        if isinstance(item_id, str) and item_id.startswith(prefix + "-"):
            try:
                numbers.append(int(item_id.split("-")[1]))
            except Exception:
                pass
    next_number = max(numbers, default=0) + 1
    return f"{prefix}-{next_number:04d}"


def get_next_car_id() -> str:
    return generate_next_id("CAR", [car["id"] for car in cars])


def get_next_part_id() -> str:
    return generate_next_id("PRT", [part["id"] for part in parts])


def get_next_customer_id() -> str:
    return generate_next_id("KUN", [customer["id"] for customer in customers])


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


# =========================================================
# Vorschlagsdatenbanken
# =========================================================
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


def update_brand_db():
    global brand_db
    values = brand_db + [car["brand"] for car in cars if car.get("brand")]
    brand_db = normalize_db_list(values)


def update_category_db():
    global category_db
    values = category_db + [part["category"] for part in parts if part.get("category")]
    category_db = normalize_db_list(values)


def make_choice_suggestions(search_text, source_list):
    text = safe_str(search_text).lower()
    if not text:
        result = source_list[:8]
    else:
        starts = [v for v in source_list if v.lower().startswith(text)]
        contains = [v for v in source_list if text in v.lower() and v not in starts]
        result = (starts + contains)[:8]
    return gr.update(choices=result, value=None)


def suggest_brand_choices(search_text):
    update_brand_db()
    return make_choice_suggestions(search_text, brand_db)


def suggest_category_choices(search_text):
    update_category_db()
    return make_choice_suggestions(search_text, category_db)


def pick_dropdown_value(value):
    return value or ""


# =========================================================
# Auswahlhilfen
# =========================================================
def get_customer_choices(include_empty: bool = True):
    choices = []
    if include_empty:
        choices.append("-")
    for customer in customers:
        choices.append(f"{customer['id']} | {customer['name']}")
    return choices


def extract_customer_id(choice: str) -> str:
    value = safe_str(choice)
    if not value or value == "-":
        return ""
    return value.split("|")[0].strip()


def get_customer_name_by_id(customer_id: str) -> str:
    for customer in customers:
        if customer["id"] == customer_id:
            return customer["name"]
    return "-"


def get_car_id_choices():
    return [car["id"] for car in cars]


def get_part_id_choices():
    return [part["id"] for part in parts]


def get_customer_id_choices():
    return [customer["id"] for customer in customers]


def get_brand_choices():
    update_brand_db()
    return brand_db


def get_category_choices():
    update_category_db()
    return category_db


# =========================================================
# Dataframes
# =========================================================
def cars_to_dataframe(data=None):
    source = data if data is not None else cars
    if not source:
        return pd.DataFrame(
            columns=[
                "ID", "Marke", "Modell", "Baujahr", "Kilometer", "Kraftstoff",
                "Farbe", "Ankauf", "Verkauf", "Gewinn", "Kunde", "Verkaufsdatum",
                "Rechnungsstatus", "Status"
            ]
        )

    rows = []
    for car in source:
        rows.append({
            "ID": car["id"],
            "Marke": car["brand"],
            "Modell": car["model"],
            "Baujahr": car["year"],
            "Kilometer": car["mileage"],
            "Kraftstoff": car["fuel"],
            "Farbe": car["color"],
            "Ankauf": format_currency(car["purchase_price"]),
            "Verkauf": format_currency(car["sale_price"]),
            "Gewinn": format_currency(calc_profit(car["purchase_price"], car["sale_price"])),
            "Kunde": get_customer_name_by_id(car.get("customer_id", "")),
            "Verkaufsdatum": car.get("sale_date", ""),
            "Rechnungsstatus": invoice_status_badge(car.get("invoice_status", "Offen")),
            "Status": car["status"],
        })
    return pd.DataFrame(rows)


def parts_to_dataframe(data=None):
    source = data if data is not None else parts
    if not source:
        return pd.DataFrame(
            columns=["ID", "Name", "Kategorie", "Marke", "Preis", "Bestand", "Gesamtwert", "Status"]
        )

    rows = []
    for part in source:
        rows.append({
            "ID": part["id"],
            "Name": part["name"],
            "Kategorie": part["category"],
            "Marke": part["brand"],
            "Preis": format_currency(part["price"]),
            "Bestand": part["stock"],
            "Gesamtwert": format_currency(float(part["price"]) * int(part["stock"])),
            "Status": part_status_badge(part["status"]),
        })
    return pd.DataFrame(rows)


def customers_to_dataframe(data=None):
    source = data if data is not None else customers
    if not source:
        return pd.DataFrame(columns=["ID", "Name", "Telefon", "E-Mail", "Adresse"])

    rows = []
    for customer in source:
        rows.append({
            "ID": customer["id"],
            "Name": customer["name"],
            "Telefon": customer["phone"],
            "E-Mail": customer["email"],
            "Adresse": customer["address"],
        })
    return pd.DataFrame(rows)


# =========================================================
# KPI / Reports
# =========================================================
def kpi_card_html(title, value, icon, accent="blue"):
    return f"""
    <div class="kpi-card {accent}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-body">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
    </div>
    """


def get_car_stats(data=None):
    source = data if data is not None else cars
    total = len(source)
    available = sum(1 for car in source if car["status"] == "Verfügbar")
    sold = sum(1 for car in source if car["status"] == "Verkauft")
    total_profit = sum(calc_profit(car["purchase_price"], car["sale_price"]) for car in source)

    if source:
        top = max(source, key=lambda x: x["sale_price"])
        top_text = f"{top['brand']} {top['model']} ({top['sale_price']:.2f} €)"
    else:
        top_text = "-"

    return str(total), str(available), str(sold), format_currency(total_profit), top_text


def get_part_stats(data=None):
    source = data if data is not None else parts
    total = len(source)
    stock = sum(int(part["stock"]) for part in source)
    total_value = sum(float(part["price"]) * int(part["stock"]) for part in source)

    if source:
        top = max(source, key=lambda x: float(x["price"]) * int(x["stock"]))
        top_text = f"{top['name']} ({format_currency(float(top['price']) * int(top['stock']))})"
    else:
        top_text = "-"

    return str(total), str(stock), format_currency(total_value), top_text


def get_customer_stats(data=None):
    source = data if data is not None else customers
    total = len(source)
    with_email = sum(1 for customer in source if safe_str(customer["email"]))
    with_phone = sum(1 for customer in source if safe_str(customer["phone"]))
    return str(total), str(with_email), str(with_phone)


def get_car_dashboard_cards(data=None):
    total, available, sold, total_profit, top_text = get_car_stats(data)
    return (
        kpi_card_html("Fahrzeuge gesamt", total, "🚗", "blue"),
        kpi_card_html("Verfügbar", available, "✅", "green"),
        kpi_card_html("Verkauft", sold, "📄", "violet"),
        kpi_card_html("Gesamtgewinn", total_profit, "💰", "gold"),
        kpi_card_html("Höchster Verkauf", top_text, "⭐", "blue"),
    )


def get_part_dashboard_cards(data=None):
    total, stock, total_value, top = get_part_stats(data)
    return (
        kpi_card_html("Teile gesamt", total, "📦", "blue"),
        kpi_card_html("Gesamtbestand", stock, "📚", "green"),
        kpi_card_html("Lagerwert", total_value, "💶", "violet"),
        kpi_card_html("Wertvollstes Teil", top, "🏆", "gold"),
    )


def get_customer_dashboard_cards(data=None):
    total, with_email, with_phone = get_customer_stats(data)
    return (
        kpi_card_html("Kunden gesamt", total, "👥", "blue"),
        kpi_card_html("Mit E-Mail", with_email, "📧", "green"),
        kpi_card_html("Mit Telefon", with_phone, "📞", "violet"),
    )


def generate_car_report(data=None):
    source = data if data is not None else cars
    if not source:
        return "Kein Fahrzeugreport möglich, da noch keine Fahrzeuge vorhanden sind."

    total = len(source)
    available = sum(1 for car in source if car["status"] == "Verfügbar")
    reserved = sum(1 for car in source if car["status"] == "Reserviert")
    sold = sum(1 for car in source if car["status"] == "Verkauft")
    total_profit = sum(calc_profit(car["purchase_price"], car["sale_price"]) for car in source)

    lines = [
        "Autozuhändler – Fahrzeugreport",
        "================================",
        f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
        "",
        f"Fahrzeuge gesamt: {total}",
        f"Verfügbar: {available}",
        f"Reserviert: {reserved}",
        f"Verkauft: {sold}",
        f"Gesamtgewinn: {format_currency(total_profit)}",
        "",
        "Fahrzeugliste:",
    ]

    for car in source:
        lines.append(
            f"- {car['id']} | {car['brand']} {car['model']} | Baujahr {car['year']} | "
            f"{car['mileage']} km | {car['fuel']} | {car['color']} | "
            f"Ankauf: {format_currency(car['purchase_price'])} | "
            f"Verkauf: {format_currency(car['sale_price'])} | "
            f"Gewinn: {format_currency(calc_profit(car['purchase_price'], car['sale_price']))} | "
            f"Kunde: {get_customer_name_by_id(car.get('customer_id', ''))} | "
            f"Rechnung: {car.get('invoice_status', 'Offen')} | Status: {car['status']}"
        )

    return "\n".join(lines)


def generate_part_report(data=None):
    source = data if data is not None else parts
    if not source:
        return "Kein Teile-Report möglich, da noch keine Teile vorhanden sind."

    total = len(source)
    total_stock = sum(int(part["stock"]) for part in source)
    total_value = sum(float(part["price"]) * int(part["stock"]) for part in source)

    lines = [
        "Autozuhändler – Teile-Report",
        "=============================",
        f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
        "",
        f"Teile gesamt: {total}",
        f"Gesamtstückzahl Lager: {total_stock}",
        f"Gesamtwert Teilelager: {format_currency(total_value)}",
        "",
        "Teileliste:",
    ]

    for part in source:
        lines.append(
            f"- {part['id']} | {part['name']} | Kategorie: {part['category']} | "
            f"Marke: {part['brand']} | Preis: {format_currency(part['price'])} | "
            f"Bestand: {part['stock']} | Status: {part['status']}"
        )

    return "\n".join(lines)


def generate_customer_report(data=None):
    source = data if data is not None else customers
    if not source:
        return "Kein Kundenreport möglich, da noch keine Kunden vorhanden sind."

    lines = [
        "Autozuhändler – Kundenreport",
        "============================",
        f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
        "",
        f"Kunden gesamt: {len(source)}",
        "",
        "Kundenliste:",
    ]

    for customer in source:
        lines.append(
            f"- {customer['id']} | {customer['name']} | Telefon: {customer['phone']} | "
            f"E-Mail: {customer['email']} | Adresse: {customer['address']}"
        )

    return "\n".join(lines)


# =========================================================
# Charts
# =========================================================
def get_empty_figure(title):
    fig, ax = plt.subplots(figsize=(8, 4.0))
    fig.patch.set_facecolor("#071224")
    ax.set_facecolor("#071224")
    ax.text(0.5, 0.5, "Noch keine Daten vorhanden", ha="center", va="center", fontsize=14, color="#cbd5e1")
    ax.set_title(title, color="white", fontsize=14, pad=16)
    ax.axis("off")
    plt.tight_layout()
    return fig


def get_car_chart(data=None):
    source = data if data is not None else cars
    counts = {"Verfügbar": 0, "Reserviert": 0, "Verkauft": 0}
    for car in source:
        if car["status"] in counts:
            counts[car["status"]] += 1

    if sum(counts.values()) == 0:
        return get_empty_figure("Fahrzeuge pro Status")

    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(8, 4.0))
    fig.patch.set_facecolor("#071224")
    ax.set_facecolor("#071224")
    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
    ax.set_title("Fahrzeuge pro Status", color="white", fontsize=14, pad=16)
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.spines["bottom"].set_color("#64748b")
    ax.spines["left"].set_color("#64748b")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.25)

    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, str(value), ha="center", va="bottom", color="white")

    plt.tight_layout()
    return fig


def get_part_chart(data=None):
    source = data if data is not None else parts
    counts = {"Verfügbar": 0, "Nachbestellen": 0, "Nicht verfügbar": 0}
    for part in source:
        counts[part["status"]] = counts.get(part["status"], 0) + int(part["stock"])

    if sum(counts.values()) == 0:
        return get_empty_figure("Teilebestand nach Status")

    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(8, 4.0))
    fig.patch.set_facecolor("#071224")
    ax.set_facecolor("#071224")
    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
    ax.set_title("Teilebestand nach Status", color="white", fontsize=14, pad=16)
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.spines["bottom"].set_color("#64748b")
    ax.spines["left"].set_color("#64748b")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.25)

    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, str(value), ha="center", va="bottom", color="white")

    plt.tight_layout()
    return fig


def get_customer_chart(data=None):
    source = data if data is not None else customers
    if not source:
        return get_empty_figure("Kundenkontakte")

    labels = ["Mit E-Mail", "Mit Telefon", "Ohne Kontakt"]
    with_email = sum(1 for c in source if safe_str(c["email"]))
    with_phone = sum(1 for c in source if safe_str(c["phone"]))
    without_contact = sum(1 for c in source if not safe_str(c["email"]) and not safe_str(c["phone"]))
    values = [with_email, with_phone, without_contact]

    fig, ax = plt.subplots(figsize=(8, 4.0))
    fig.patch.set_facecolor("#071224")
    ax.set_facecolor("#071224")
    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
    ax.set_title("Kundenkontakte", color="white", fontsize=14, pad=16)
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.spines["bottom"].set_color("#64748b")
    ax.spines["left"].set_color("#64748b")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.25)

    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, str(value), ha="center", va="bottom", color="white")

    plt.tight_layout()
    return fig


# =========================================================
# Refresh-Helfer
# =========================================================
def refresh_car_view(filtered_data=None, status_message=""):
    data = filtered_data if filtered_data is not None else cars
    return (
        status_message,
        cars_to_dataframe(data),
        generate_car_report(data) if data else "Keine passenden Fahrzeuge gefunden.",
        *get_car_dashboard_cards(data),
        get_car_chart(data),
        gr.update(choices=["Alle"] + get_brand_choices(), value="Alle"),
        gr.update(choices=get_car_id_choices(), value=None),
        gr.update(choices=get_customer_choices(), value="-"),
        get_next_car_id(),
    )


def refresh_part_view(filtered_data=None, status_message=""):
    data = filtered_data if filtered_data is not None else parts
    return (
        status_message,
        parts_to_dataframe(data),
        generate_part_report(data) if data else "Keine passenden Teile gefunden.",
        *get_part_dashboard_cards(data),
        get_part_chart(data),
        gr.update(choices=["Alle"] + get_category_choices(), value="Alle"),
        gr.update(choices=get_part_id_choices(), value=None),
        get_next_part_id(),
    )


def refresh_customer_view(filtered_data=None, status_message=""):
    data = filtered_data if filtered_data is not None else customers
    return (
        status_message,
        customers_to_dataframe(data),
        generate_customer_report(data) if data else "Keine passenden Kunden gefunden.",
        *get_customer_dashboard_cards(data),
        get_customer_chart(data),
        gr.update(choices=get_customer_id_choices(), value=None),
        gr.update(choices=get_customer_choices(), value="-"),
        get_next_customer_id(),
    )


# =========================================================
# Login
# =========================================================
def login_user(username, password):
    username = safe_str(username)
    password = safe_str(password)

    if username not in EMPLOYEES:
        return (
            "Unbekannter Benutzer.",
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            ""
        )

    user = EMPLOYEES[username]
    if password != user["password"]:
        return (
            "Falsches Passwort.",
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            ""
        )

    welcome = f"Angemeldet als {user['name']} ({user['role']})"
    return (
        welcome,
        gr.update(visible=False),
        gr.update(visible=True),
        user["name"],
        user["role"],
    )


def logout_user():
    return (
        "Abgemeldet.",
        gr.update(visible=True),
        gr.update(visible=False),
        "",
        ""
    )


# =========================================================
# Autos CRUD
# =========================================================
def clear_car_form():
    return (
        get_next_car_id(),  # car_id
        "",                 # car_brand
        "",                 # car_model
        None,               # car_fuel
        "",                 # car_year
        "",                 # car_mileage
        "",                 # car_color
        "",                 # car_purchase_price
        "",                 # car_sale_price
        "-",                # car_customer
        "Offen",            # car_invoice_status
        None,               # car_status
    )


def add_car(
    car_id, brand, model, year, mileage, fuel, color,
    purchase_price, sale_price, customer_choice, invoice_status, status
):
    car_id = safe_str(car_id).upper() or get_next_car_id()
    brand = smart_capitalize(brand)
    model = smart_capitalize(model)
    color = smart_capitalize(color)
    customer_id = extract_customer_id(customer_choice)

    if not all([brand, model, year, mileage, fuel, color, purchase_price, sale_price, invoice_status, status]):
        return (
            *refresh_car_view(status_message="Bitte alle Pflichtfelder ausfüllen."),
            car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
        )

    try:
        year = int(year)
        mileage = int(mileage)
        purchase_price = float(purchase_price)
        sale_price = float(sale_price)
    except ValueError:
        return (
            *refresh_car_view(status_message="Baujahr und Kilometerstand müssen ganze Zahlen sein. Preise müssen Zahlen sein."),
            car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
        )

    if year < 1900 or mileage < 0 or purchase_price < 0 or sale_price < 0:
        return (
            *refresh_car_view(status_message="Bitte gültige Werte eingeben."),
            car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
        )

    if any(car["id"] == car_id for car in cars):
        return (
            *refresh_car_view(status_message=f"Die Fahrzeug-ID '{car_id}' existiert bereits."),
            car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
        )

    sale_date = datetime.now().strftime("%d.%m.%Y") if status == "Verkauft" else ""

    cars.append({
        "id": car_id,
        "brand": brand,
        "model": model,
        "year": year,
        "mileage": mileage,
        "fuel": fuel,
        "color": color,
        "purchase_price": purchase_price,
        "sale_price": sale_price,
        "customer_id": customer_id,
        "sale_date": sale_date,
        "invoice_status": invoice_status,
        "status": status,
    })
    update_brand_db()

    return (
        *refresh_car_view(status_message=f"Fahrzeug '{brand} {model}' wurde gespeichert."),
        *clear_car_form()
    )


def load_car_for_edit(selected_id):
    if not selected_id:
        return "", "", "", None, "", "", "", "", "-", "Offen", None, "Bitte zuerst ein Fahrzeug auswählen."

    for car in cars:
        if car["id"] == selected_id:
            customer_value = "-"
            if car.get("customer_id"):
                customer_name = get_customer_name_by_id(car["customer_id"])
                customer_value = f"{car['customer_id']} | {customer_name}"

            return (
                car["id"],
                car["brand"],
                car["model"],
                car["fuel"],
                str(car["year"]),
                str(car["mileage"]),
                car["color"],
                str(car["purchase_price"]),
                str(car["sale_price"]),
                customer_value,
                car["invoice_status"],
                car["status"],
                f"Fahrzeug '{selected_id}' geladen."
            )

    return "", "", "", None, "", "", "", "", "-", "Offen", None, "Fahrzeug nicht gefunden."


def update_car(
    selected_id, car_id, brand, model, fuel, year, mileage, color,
    purchase_price, sale_price, customer_choice, invoice_status, status
):
    if not selected_id:
        return (
            *refresh_car_view(status_message="Bitte zuerst ein Fahrzeug zum Bearbeiten auswählen."),
            car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
        )

    brand = smart_capitalize(brand)
    model = smart_capitalize(model)
    color = smart_capitalize(color)
    customer_id = extract_customer_id(customer_choice)

    if not all([brand, model, fuel, year, mileage, color, purchase_price, sale_price, invoice_status, status]):
        return (
            *refresh_car_view(status_message="Bitte alle Pflichtfelder ausfüllen."),
            car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
        )

    try:
        year = int(year)
        mileage = int(mileage)
        purchase_price = float(purchase_price)
        sale_price = float(sale_price)
    except ValueError:
        return (
            *refresh_car_view(status_message="Baujahr und Kilometerstand müssen ganze Zahlen sein. Preise müssen Zahlen sein."),
            car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
        )

    for car in cars:
        if car["id"] == selected_id:
            car["brand"] = brand
            car["model"] = model
            car["fuel"] = fuel
            car["year"] = year
            car["mileage"] = mileage
            car["color"] = color
            car["purchase_price"] = purchase_price
            car["sale_price"] = sale_price
            car["customer_id"] = customer_id
            car["invoice_status"] = invoice_status
            car["status"] = status
            car["sale_date"] = datetime.now().strftime("%d.%m.%Y") if status == "Verkauft" else ""
            update_brand_db()

            return (
                *refresh_car_view(status_message=f"Fahrzeug '{selected_id}' wurde aktualisiert."),
                car["id"], car["brand"], car["model"], car["fuel"], str(car["year"]),
                str(car["mileage"]), car["color"], str(car["purchase_price"]), str(car["sale_price"]),
                customer_choice, car["invoice_status"], car["status"]
            )

    return (
        *refresh_car_view(status_message="Fahrzeug nicht gefunden."),
        car_id, brand, model, fuel, year, mileage, color, purchase_price, sale_price, customer_choice, invoice_status, status
    )


def delete_car(selected_id):
    if not selected_id:
        return (
            *refresh_car_view(status_message="Bitte zuerst ein Fahrzeug auswählen."),
            *clear_car_form()
        )

    for index, car in enumerate(cars):
        if car["id"] == selected_id:
            deleted_text = f"{car['brand']} {car['model']}"
            del cars[index]
            update_brand_db()
            return (
                *refresh_car_view(status_message=f"Fahrzeug '{selected_id}' ({deleted_text}) wurde gelöscht."),
                *clear_car_form()
            )

    return (
        *refresh_car_view(status_message="Fahrzeug nicht gefunden."),
        *clear_car_form()
    )


def filter_cars(search_term, brand_filter, status_filter):
    filtered = cars

    term = safe_str(search_term).lower()
    if term:
        filtered = [
            car for car in filtered
            if term in car["id"].lower()
            or term in car["brand"].lower()
            or term in car["model"].lower()
            or term in car["fuel"].lower()
            or term in car["color"].lower()
            or term in car["status"].lower()
            or term in get_customer_name_by_id(car.get("customer_id", "")).lower()
        ]

    if brand_filter != "Alle":
        filtered = [car for car in filtered if car["brand"] == brand_filter]

    if status_filter != "Alle":
        filtered = [car for car in filtered if car["status"] == status_filter]

    return (
        cars_to_dataframe(filtered),
        generate_car_report(filtered) if filtered else "Keine passenden Fahrzeuge gefunden.",
        *get_car_dashboard_cards(filtered),
        get_car_chart(filtered),
    )


# =========================================================
# Teile CRUD
# =========================================================
def clear_part_form():
    return get_next_part_id(), "", "", "", "", "", None


def add_part(part_id, name, category, brand, price, stock, status):
    part_id = safe_str(part_id).upper() or get_next_part_id()
    name = smart_capitalize(name)
    category = smart_capitalize(category)
    brand = smart_capitalize(brand)

    if not all([name, category, brand, price, stock, status]):
        return (
            *refresh_part_view(status_message="Bitte alle Felder ausfüllen."),
            part_id, name, category, brand, price, stock, status
        )

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        return (
            *refresh_part_view(status_message="Preis muss eine Zahl sein, Bestand eine ganze Zahl."),
            part_id, name, category, brand, price, stock, status
        )

    if price < 0 or stock < 0:
        return (
            *refresh_part_view(status_message="Bitte gültige Werte eingeben."),
            part_id, name, category, brand, price, stock, status
        )

    if any(part["id"] == part_id for part in parts):
        return (
            *refresh_part_view(status_message=f"Die Teile-ID '{part_id}' existiert bereits."),
            part_id, name, category, brand, price, stock, status
        )

    parts.append({
        "id": part_id,
        "name": name,
        "category": category,
        "brand": brand,
        "price": price,
        "stock": stock,
        "status": status,
    })
    update_category_db()

    return (
        *refresh_part_view(status_message=f"Teil '{name}' wurde gespeichert."),
        *clear_part_form()
    )


def load_part_for_edit(selected_id):
    if not selected_id:
        return "", "", "", "", "", "", None, "Bitte zuerst ein Teil auswählen."

    for part in parts:
        if part["id"] == selected_id:
            return (
                part["id"],
                part["name"],
                part["category"],
                part["brand"],
                str(part["price"]),
                str(part["stock"]),
                part["status"],
                f"Teil '{selected_id}' geladen."
            )

    return "", "", "", "", "", "", None, "Teil nicht gefunden."


def update_part(selected_id, part_id, name, category, brand, price, stock, status):
    if not selected_id:
        return (
            *refresh_part_view(status_message="Bitte zuerst ein Teil zum Bearbeiten auswählen."),
            part_id, name, category, brand, price, stock, status
        )

    name = smart_capitalize(name)
    category = smart_capitalize(category)
    brand = smart_capitalize(brand)

    if not all([name, category, brand, price, stock, status]):
        return (
            *refresh_part_view(status_message="Bitte alle Felder korrekt ausfüllen."),
            part_id, name, category, brand, price, stock, status
        )

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        return (
            *refresh_part_view(status_message="Preis muss eine Zahl sein, Bestand eine ganze Zahl."),
            part_id, name, category, brand, price, stock, status
        )

    for part in parts:
        if part["id"] == selected_id:
            part["name"] = name
            part["category"] = category
            part["brand"] = brand
            part["price"] = price
            part["stock"] = stock
            part["status"] = status
            update_category_db()

            return (
                *refresh_part_view(status_message=f"Teil '{selected_id}' wurde aktualisiert."),
                part["id"], part["name"], part["category"], part["brand"], str(part["price"]), str(part["stock"]), part["status"]
            )

    return (
        *refresh_part_view(status_message="Teil nicht gefunden."),
        part_id, name, category, brand, price, stock, status
    )


def delete_part(selected_id):
    if not selected_id:
        return (
            *refresh_part_view(status_message="Bitte zuerst ein Teil auswählen."),
            *clear_part_form()
        )

    for index, part in enumerate(parts):
        if part["id"] == selected_id:
            deleted_text = part["name"]
            del parts[index]
            update_category_db()
            return (
                *refresh_part_view(status_message=f"Teil '{selected_id}' ({deleted_text}) wurde gelöscht."),
                *clear_part_form()
            )

    return (
        *refresh_part_view(status_message="Teil nicht gefunden."),
        *clear_part_form()
    )


def filter_parts(search_term, category_filter, status_filter):
    filtered = parts
    term = safe_str(search_term).lower()

    if term:
        filtered = [
            part for part in filtered
            if term in part["id"].lower()
            or term in part["name"].lower()
            or term in part["category"].lower()
            or term in part["brand"].lower()
            or term in part["status"].lower()
        ]

    if category_filter != "Alle":
        filtered = [part for part in filtered if part["category"] == category_filter]

    if status_filter != "Alle":
        filtered = [part for part in filtered if part["status"] == status_filter]

    return (
        parts_to_dataframe(filtered),
        generate_part_report(filtered) if filtered else "Keine passenden Teile gefunden.",
        *get_part_dashboard_cards(filtered),
        get_part_chart(filtered),
    )


# =========================================================
# Kunden CRUD
# =========================================================
def clear_customer_form():
    return get_next_customer_id(), "", "", "", ""


def add_customer(customer_id, name, phone, email, address):
    customer_id = safe_str(customer_id).upper() or get_next_customer_id()
    name = smart_capitalize(name)
    address = smart_capitalize(address)

    if not name:
        return (
            *refresh_customer_view(status_message="Bitte mindestens den Kundennamen eingeben."),
            customer_id, name, phone, email, address
        )

    if any(customer["id"] == customer_id for customer in customers):
        return (
            *refresh_customer_view(status_message=f"Die Kunden-ID '{customer_id}' existiert bereits."),
            customer_id, name, phone, email, address
        )

    customers.append({
        "id": customer_id,
        "name": name,
        "phone": safe_str(phone),
        "email": safe_str(email),
        "address": address,
    })

    return (
        *refresh_customer_view(status_message=f"Kunde '{name}' wurde gespeichert."),
        *clear_customer_form()
    )


def load_customer_for_edit(selected_id):
    if not selected_id:
        return "", "", "", "", "", "Bitte zuerst einen Kunden auswählen."

    for customer in customers:
        if customer["id"] == selected_id:
            return (
                customer["id"],
                customer["name"],
                customer["phone"],
                customer["email"],
                customer["address"],
                f"Kunde '{selected_id}' geladen."
            )

    return "", "", "", "", "", "Kunde nicht gefunden."


def update_customer(selected_id, customer_id, name, phone, email, address):
    if not selected_id:
        return (
            *refresh_customer_view(status_message="Bitte zuerst einen Kunden zum Bearbeiten auswählen."),
            customer_id, name, phone, email, address
        )

    name = smart_capitalize(name)
    address = smart_capitalize(address)

    if not name:
        return (
            *refresh_customer_view(status_message="Bitte mindestens den Kundennamen eingeben."),
            customer_id, name, phone, email, address
        )

    for customer in customers:
        if customer["id"] == selected_id:
            customer["name"] = name
            customer["phone"] = safe_str(phone)
            customer["email"] = safe_str(email)
            customer["address"] = address

            return (
                *refresh_customer_view(status_message=f"Kunde '{selected_id}' wurde aktualisiert."),
                customer["id"], customer["name"], customer["phone"], customer["email"], customer["address"]
            )

    return (
        *refresh_customer_view(status_message="Kunde nicht gefunden."),
        customer_id, name, phone, email, address
    )


def delete_customer(selected_id):
    if not selected_id:
        return (
            *refresh_customer_view(status_message="Bitte zuerst einen Kunden auswählen."),
            *clear_customer_form()
        )

    # Kunde darf nicht gelöscht werden, wenn er einem verkauften Auto zugeordnet ist
    used_by_car = next((car for car in cars if car.get("customer_id") == selected_id), None)
    if used_by_car:
        return (
            *refresh_customer_view(
                status_message=f"Kunde '{selected_id}' ist noch mit Fahrzeug '{used_by_car['id']}' verknüpft und kann nicht gelöscht werden."
            ),
            *clear_customer_form()
        )

    for index, customer in enumerate(customers):
        if customer["id"] == selected_id:
            deleted_text = customer["name"]
            del customers[index]
            return (
                *refresh_customer_view(status_message=f"Kunde '{selected_id}' ({deleted_text}) wurde gelöscht."),
                *clear_customer_form()
            )

    return (
        *refresh_customer_view(status_message="Kunde nicht gefunden."),
        *clear_customer_form()
    )


def filter_customers(search_term):
    filtered = customers
    term = safe_str(search_term).lower()
    if term:
        filtered = [
            customer for customer in filtered
            if term in customer["id"].lower()
            or term in customer["name"].lower()
            or term in customer["phone"].lower()
            or term in customer["email"].lower()
            or term in customer["address"].lower()
        ]

    return (
        customers_to_dataframe(filtered),
        generate_customer_report(filtered) if filtered else "Keine passenden Kunden gefunden.",
        *get_customer_dashboard_cards(filtered),
        get_customer_chart(filtered),
    )


# =========================================================
# Exporte
# =========================================================
def export_text_report(filename_prefix: str, text: str) -> str:
    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = NEXTCLOUD_EXPORT_DIR / filename
    filepath.write_text(text, encoding="utf-8")
    return f"Export erfolgreich in Nextcloud:\n{filepath}"


def export_dataframe_csv(df: pd.DataFrame, filename_prefix: str) -> str:
    if df.empty:
        return "Kein CSV-Export durchgeführt: Keine Daten vorhanden."
    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = NEXTCLOUD_EXPORT_DIR / filename
    df.to_csv(filepath, index=False, encoding="utf-8-sig", sep=";")
    return f"CSV exportiert:\n{filepath}"


def export_dataframe_excel(df: pd.DataFrame, filename_prefix: str) -> str:
    if df.empty:
        return "Kein Excel-Export durchgeführt: Keine Daten vorhanden."
    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = NEXTCLOUD_EXPORT_DIR / filename
    df.to_excel(filepath, index=False)
    return f"Excel exportiert:\n{filepath}"


def export_cars_txt():
    return export_text_report("fahrzeugreport", generate_car_report())


def export_parts_txt():
    return export_text_report("teile_report", generate_part_report())


def export_customers_txt():
    return export_text_report("kunden_report", generate_customer_report())


def export_cars_csv():
    return export_dataframe_csv(cars_to_dataframe(), "fahrzeuge")


def export_parts_csv():
    return export_dataframe_csv(parts_to_dataframe(), "teile")


def export_customers_csv():
    return export_dataframe_csv(customers_to_dataframe(), "kunden")


def export_cars_excel():
    return export_dataframe_excel(cars_to_dataframe(), "fahrzeuge")


def export_parts_excel():
    return export_dataframe_excel(parts_to_dataframe(), "teile")


def export_customers_excel():
    return export_dataframe_excel(customers_to_dataframe(), "kunden")


# =========================================================
# Initial Load
# =========================================================
def initial_load():
    update_brand_db()
    update_category_db()

    return (
        *get_car_dashboard_cards(),
        cars_to_dataframe(),
        generate_car_report(),
        get_car_chart(),
        gr.update(choices=["Alle"] + get_brand_choices(), value="Alle"),
        gr.update(choices=get_car_id_choices(), value=None),
        gr.update(choices=get_customer_choices(), value="-"),
        get_next_car_id(),

        *get_part_dashboard_cards(),
        parts_to_dataframe(),
        generate_part_report(),
        get_part_chart(),
        gr.update(choices=["Alle"] + get_category_choices(), value="Alle"),
        gr.update(choices=get_part_id_choices(), value=None),
        get_next_part_id(),

        *get_customer_dashboard_cards(),
        customers_to_dataframe(),
        generate_customer_report(),
        get_customer_chart(),
        gr.update(choices=get_customer_id_choices(), value=None),
        get_next_customer_id(),
    )


# =========================================================
# CSS
# =========================================================
custom_css = """
:root {
    --bg: #030712;
    --panel: #071224;
    --panel-2: #0b1730;
    --panel-3: #0f1d3b;
    --border: rgba(148, 163, 184, 0.18);
    --text: #f8fafc;
    --muted: #cbd5e1;
}

.gradio-container {
    background: linear-gradient(135deg, #020617 0%, #071224 45%, #0b1020 100%) !important;
    color: var(--text) !important;
}

#dashboard-root, #dashboard-root * {
    box-sizing: border-box;
}

#dashboard-root .gr-block, #dashboard-root .block {
    border-radius: 20px !important;
    border: 1px solid var(--border) !important;
    background: rgba(7, 18, 36, 0.92) !important;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.28) !important;
}

#dashboard-root .gr-row, #dashboard-root .gr-column, #dashboard-root .gr-group, #dashboard-root .gr-box {
    overflow: visible !important;
}

#dashboard-root h1, #dashboard-root h2, #dashboard-root h3, #dashboard-root h4, #dashboard-root p, #dashboard-root label {
    color: var(--text) !important;
}

.main-title {
    padding: 8px 4px 18px 4px;
}

.main-title h1 {
    font-size: 36px !important;
    font-weight: 800 !important;
    margin-bottom: 6px !important;
}

.main-title p {
    color: var(--muted) !important;
    margin: 0 !important;
    font-size: 15px !important;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
}

.subtle-text {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 10px;
}

.kpi-card {
    display: flex;
    align-items: center;
    gap: 14px;
    min-height: 92px;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: linear-gradient(145deg, rgba(10,18,35,0.96), rgba(16,29,58,0.92));
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.26);
}

.kpi-card.blue { border-color: rgba(56, 189, 248, 0.20); }
.kpi-card.green { border-color: rgba(34, 197, 94, 0.20); }
.kpi-card.violet { border-color: rgba(139, 92, 246, 0.20); }
.kpi-card.gold { border-color: rgba(245, 158, 11, 0.20); }

.kpi-icon {
    min-width: 52px;
    height: 52px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.06);
    font-size: 24px;
}

.kpi-body {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.kpi-title {
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}

.kpi-value {
    color: var(--text);
    font-size: 18px;
    font-weight: 800;
    line-height: 1.2;
    word-break: break-word;
}

#dashboard-root input, #dashboard-root textarea {
    background: rgba(15, 23, 42, 0.92) !important;
    color: #ffffff !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    border-radius: 14px !important;
}

#dashboard-root input:focus, #dashboard-root textarea:focus {
    border-color: rgba(56, 189, 248, 0.65) !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.16) !important;
}

#dashboard-root .primary-btn button,
#dashboard-root .secondary-btn button,
#dashboard-root .danger-btn button {
    border-radius: 14px !important;
    font-weight: 700 !important;
    transition: all 0.18s ease !important;
}

#dashboard-root .primary-btn button:hover,
#dashboard-root .secondary-btn button:hover,
#dashboard-root .danger-btn button:hover {
    transform: translateY(-1px);
}

#dashboard-root [role="listbox"], #dashboard-root .options, #dashboard-root .wrap, #dashboard-root .dropdown, #dashboard-root .menu {
    z-index: 9999 !important;
}

#dashboard-root .gr-dataframe {
    border-radius: 18px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: rgba(7, 18, 36, 0.95) !important;
}

#dashboard-root table {
    border-radius: 18px !important;
    overflow: hidden !important;
}

#dashboard-root thead tr th {
    background: rgba(15, 29, 59, 0.96) !important;
    color: #f8fafc !important;
    font-weight: 700 !important;
    border-bottom: 1px solid rgba(148,163,184,0.16) !important;
}

#dashboard-root tbody tr {
    background: rgba(7, 18, 36, 0.88) !important;
}

#dashboard-root tbody tr:nth-child(even) {
    background: rgba(10, 20, 40, 0.95) !important;
}

#dashboard-root tbody td {
    color: #e2e8f0 !important;
    border-bottom: 1px solid rgba(148,163,184,0.08) !important;
}

.report-box textarea {
    font-family: Consolas, monospace !important;
    line-height: 1.45 !important;
}

.legend-box {
    padding: 12px 14px;
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(148, 163, 184, 0.18);
    color: #e2e8f0;
}

footer {
    display: none !important;
}
"""

# =========================================================
# UI
# =========================================================
with gr.Blocks(title=APP_TITLE, elem_id="dashboard-root") as demo:
    current_user_name = gr.State("")
    current_user_role = gr.State("")

    login_container = gr.Column(visible=True)
    app_container = gr.Column(visible=False)

    with login_container:
        gr.HTML("""
        <div class="main-title">
            <h1>Autozuhändler</h1>
            <p>Mitarbeiter-Login für Fahrzeuge, Teile, Kunden und Verkaufsverwaltung.</p>
        </div>
        """)
        with gr.Row():
            with gr.Column(scale=1):
                login_username = gr.Textbox(label="Benutzername")
                login_password = gr.Textbox(label="Passwort", type="password")
                login_btn = gr.Button("Anmelden", variant="primary", elem_classes=["primary-btn"])
                login_status = gr.Textbox(label="Status", interactive=False)
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="legend-box">
                    <b>Demo-Zugänge</b><br><br>
                    Julian / admin123<br>
                    Fabienne / admin456<br>
                    Mikail / admin789<br>
                    Sirin / admin000<br>
                    lehrer / lehrer123
                </div>
                """)

    with app_container:
        gr.HTML("""
        <div class="main-title">
            <h1>Autozuhändler</h1>
            <p>Verwaltung von Fahrzeugen, Teilen, Kunden, Verkauf, Rechnungsstatus und Exporten.</p>
        </div>
        """)

        with gr.Row():
            user_info = gr.Textbox(label="Angemeldeter Mitarbeiter", interactive=False)
            user_role = gr.Textbox(label="Rolle", interactive=False)
            logout_btn = gr.Button("Abmelden", elem_classes=["secondary-btn"])

        with gr.Tab("Fahrzeuge"):
            with gr.Row():
                car_kpi_1 = gr.HTML()
                car_kpi_2 = gr.HTML()
                car_kpi_3 = gr.HTML()
                car_kpi_4 = gr.HTML()
                car_kpi_5 = gr.HTML()

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">🚘 Fahrzeug anlegen / bearbeiten</div><div class="subtle-text">Automatische ID, Ankauf, Verkauf, Gewinn, Kunde und Rechnungsstatus.</div>')

                    car_edit_select = gr.Dropdown(label="Fahrzeug wählen", choices=[], value=None)
                    with gr.Row():
                        car_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                        car_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                    car_id = gr.Textbox(label="Fahrzeug-ID", interactive=False, value=get_next_car_id())
                    car_brand = gr.Textbox(label="Marke")
                    car_brand_suggestions = gr.Dropdown(label="Marken-Vorschläge", choices=[], value=None)
                    car_model = gr.Textbox(label="Modell")
                    car_year = gr.Textbox(label="Baujahr")
                    car_mileage = gr.Textbox(label="Kilometerstand")
                    car_fuel = gr.Dropdown(choices=FUELS, label="Kraftstoff", value=None)
                    car_color = gr.Textbox(label="Farbe")
                    car_purchase_price = gr.Textbox(label="Ankaufspreis")
                    car_sale_price = gr.Textbox(label="Verkaufspreis")
                    car_customer = gr.Dropdown(label="Kunde", choices=get_customer_choices(), value="-")
                    car_invoice_status = gr.Dropdown(choices=INVOICE_STATUSES, label="Rechnungsstatus", value="Offen")
                    car_status = gr.Dropdown(choices=CAR_STATUSES, label="Status", value=None)

                    with gr.Row():
                        car_add_btn = gr.Button("Neues Fahrzeug speichern", variant="primary", elem_classes=["primary-btn"])
                        car_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                        car_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                    car_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                with gr.Column(scale=2):
                    gr.HTML('<div class="section-title">📋 Fahrzeugbestand</div><div class="subtle-text">Suche nach ID, Marke, Kunde, Status und Verkaufsstand.</div>')
                    car_table = gr.Dataframe(interactive=False, label="Fahrzeugbestand")

            with gr.Row():
                car_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Marke, Modell, Kunde, Status")
                car_brand_filter = gr.Dropdown(label="🏷️ Marke filtern", choices=["Alle"] + get_brand_choices(), value="Alle", filterable=True)
                car_status_filter = gr.Dropdown(label="📌 Status filtern", choices=["Alle"] + CAR_STATUSES, value="Alle")

            with gr.Row():
                car_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                car_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">🧾 Fahrzeugreport</div>')
                    car_report = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">📊 Auswertung</div>')
                    car_chart = gr.Plot(label="Fahrzeuge pro Status")

            with gr.Row():
                car_export_txt_btn = gr.Button("TXT exportieren in Nextcloud", variant="primary", elem_classes=["primary-btn"])
                car_export_csv_btn = gr.Button("CSV exportieren", elem_classes=["secondary-btn"])
                car_export_xlsx_btn = gr.Button("Excel exportieren", elem_classes=["secondary-btn"])
            car_export_status = gr.Textbox(label="Exportstatus", interactive=False)

        with gr.Tab("Teile"):
            with gr.Row():
                part_kpi_1 = gr.HTML()
                part_kpi_2 = gr.HTML()
                part_kpi_3 = gr.HTML()
                part_kpi_4 = gr.HTML()

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">📦 Teil anlegen / bearbeiten</div><div class="subtle-text">Mit Ampel-Status für Lagerverfügbarkeit.</div>')

                    part_edit_select = gr.Dropdown(label="Teil wählen", choices=[], value=None)
                    with gr.Row():
                        part_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                        part_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                    part_id = gr.Textbox(label="Teile-ID", interactive=False, value=get_next_part_id())
                    part_name = gr.Textbox(label="Teilename")
                    part_category = gr.Textbox(label="Kategorie")
                    part_category_suggestions = gr.Dropdown(label="Kategorie-Vorschläge", choices=[], value=None)
                    part_brand = gr.Textbox(label="Marke / Hersteller")
                    part_price = gr.Textbox(label="Preis")
                    part_stock = gr.Textbox(label="Bestand")
                    part_status = gr.Dropdown(choices=PART_STATUSES, label="Lagerstatus", value=None)

                    gr.HTML("""
                    <div class="legend-box">
                        <b>Ampelstatus</b><br>
                        🟢 Verfügbar<br>
                        🟡 Nachbestellen<br>
                        🔴 Nicht verfügbar
                    </div>
                    """)

                    with gr.Row():
                        part_add_btn = gr.Button("Neues Teil speichern", variant="primary", elem_classes=["primary-btn"])
                        part_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                        part_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                    part_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                with gr.Column(scale=2):
                    gr.HTML('<div class="section-title">🗂️ Teilelager</div><div class="subtle-text">Lagerwert, Bestand und Ampelstatus.</div>')
                    part_table = gr.Dataframe(interactive=False, label="Teilebestand")

            with gr.Row():
                part_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Name, Kategorie, Marke, Status")
                part_category_filter = gr.Dropdown(label="🏷️ Kategorie filtern", choices=["Alle"] + get_category_choices(), value="Alle", filterable=True)
                part_status_filter = gr.Dropdown(label="📌 Status filtern", choices=["Alle"] + PART_STATUSES, value="Alle")

            with gr.Row():
                part_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                part_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">🧾 Teile-Report</div>')
                    part_report = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">📊 Auswertung</div>')
                    part_chart = gr.Plot(label="Teilebestand nach Status")

            with gr.Row():
                part_export_txt_btn = gr.Button("TXT exportieren in Nextcloud", variant="primary", elem_classes=["primary-btn"])
                part_export_csv_btn = gr.Button("CSV exportieren", elem_classes=["secondary-btn"])
                part_export_xlsx_btn = gr.Button("Excel exportieren", elem_classes=["secondary-btn"])
            part_export_status = gr.Textbox(label="Exportstatus", interactive=False)

        with gr.Tab("Kunden"):
            with gr.Row():
                customer_kpi_1 = gr.HTML()
                customer_kpi_2 = gr.HTML()
                customer_kpi_3 = gr.HTML()

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">👤 Kunde anlegen / bearbeiten</div><div class="subtle-text">Automatische Kunden-ID und Zuordnung zu Verkäufen.</div>')

                    customer_edit_select = gr.Dropdown(label="Kunde wählen", choices=[], value=None)
                    with gr.Row():
                        customer_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                        customer_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                    customer_id = gr.Textbox(label="Kunden-ID", interactive=False, value=get_next_customer_id())
                    customer_name = gr.Textbox(label="Name")
                    customer_phone = gr.Textbox(label="Telefon")
                    customer_email = gr.Textbox(label="E-Mail")
                    customer_address = gr.Textbox(label="Adresse", lines=3)

                    with gr.Row():
                        customer_add_btn = gr.Button("Neuen Kunden speichern", variant="primary", elem_classes=["primary-btn"])
                        customer_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                        customer_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                    customer_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                with gr.Column(scale=2):
                    gr.HTML('<div class="section-title">👥 Kundenverwaltung</div><div class="subtle-text">Alle Kunden mit Kontaktübersicht.</div>')
                    customer_table = gr.Dataframe(interactive=False, label="Kunden")

            with gr.Row():
                customer_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Name, Telefon, E-Mail, Adresse")
                customer_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                customer_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">🧾 Kundenreport</div>')
                    customer_report = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">📊 Auswertung</div>')
                    customer_chart = gr.Plot(label="Kundenkontakte")

            with gr.Row():
                customer_export_txt_btn = gr.Button("TXT exportieren in Nextcloud", variant="primary", elem_classes=["primary-btn"])
                customer_export_csv_btn = gr.Button("CSV exportieren", elem_classes=["secondary-btn"])
                customer_export_xlsx_btn = gr.Button("Excel exportieren", elem_classes=["secondary-btn"])
            customer_export_status = gr.Textbox(label="Exportstatus", interactive=False)

    # Initial Load
    demo.load(
        fn=initial_load,
        outputs=[
            car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_table, car_report, car_chart, car_brand_filter, car_edit_select, car_customer, car_id,

            part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_table, part_report, part_chart, part_category_filter, part_edit_select, part_id,

            customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_table, customer_report, customer_chart, customer_edit_select, customer_id,
        ],
    )

    # Login
    login_btn.click(
        fn=login_user,
        inputs=[login_username, login_password],
        outputs=[login_status, login_container, app_container, user_info, user_role],
    )

    logout_btn.click(
        fn=logout_user,
        inputs=[],
        outputs=[login_status, login_container, app_container, user_info, user_role],
    )

    # Live formatting
    car_brand.blur(fn=smart_capitalize, inputs=[car_brand], outputs=[car_brand])
    car_model.blur(fn=smart_capitalize, inputs=[car_model], outputs=[car_model])
    car_color.blur(fn=smart_capitalize, inputs=[car_color], outputs=[car_color])

    part_name.blur(fn=smart_capitalize, inputs=[part_name], outputs=[part_name])
    part_category.blur(fn=smart_capitalize, inputs=[part_category], outputs=[part_category])
    part_brand.blur(fn=smart_capitalize, inputs=[part_brand], outputs=[part_brand])

    customer_name.blur(fn=smart_capitalize, inputs=[customer_name], outputs=[customer_name])
    customer_address.blur(fn=smart_capitalize, inputs=[customer_address], outputs=[customer_address])

    # Suggestions via Dropdown
    car_brand.change(fn=suggest_brand_choices, inputs=[car_brand], outputs=[car_brand_suggestions])
    car_brand_suggestions.change(fn=pick_dropdown_value, inputs=[car_brand_suggestions], outputs=[car_brand])

    part_category.change(fn=suggest_category_choices, inputs=[part_category], outputs=[part_category_suggestions])
    part_category_suggestions.change(fn=pick_dropdown_value, inputs=[part_category_suggestions], outputs=[part_category])

    # Cars
    car_add_btn.click(
        fn=add_car,
        inputs=[
            car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color,
            car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
        outputs=[
            car_status_msg, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_chart, car_brand_filter, car_edit_select, car_customer, car_id,
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
        
    )

    car_load_btn.click(
        fn=load_car_for_edit,
        inputs=[car_edit_select],
        outputs=[
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage, car_color,
            car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status, car_status_msg
        ],
    )

    car_update_btn.click(
        fn=update_car,
        inputs=[
            car_edit_select, car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
        outputs=[
            car_status_msg, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_chart, car_brand_filter, car_edit_select, car_customer, car_id,
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
    )

    car_delete_btn.click(
        fn=delete_car,
        inputs=[car_edit_select],
        outputs=[
            car_status_msg, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_chart, car_brand_filter, car_edit_select, car_customer, car_id,
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
    )

    car_clear_btn.click(
        fn=clear_car_form,
        outputs=[
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
    )

    car_filter_btn.click(
        fn=filter_cars,
        inputs=[car_search, car_brand_filter, car_status_filter],
        outputs=[car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5, car_chart],
    )

    car_reset_btn.click(
        fn=lambda: ("", "Alle", "Alle", cars_to_dataframe(), generate_car_report(), *get_car_dashboard_cards(), get_car_chart()),
        inputs=[],
        outputs=[car_search, car_brand_filter, car_status_filter, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5, car_chart],
    )

    car_export_txt_btn.click(fn=export_cars_txt, outputs=[car_export_status])
    car_export_csv_btn.click(fn=export_cars_csv, outputs=[car_export_status])
    car_export_xlsx_btn.click(fn=export_cars_excel, outputs=[car_export_status])

    # Parts
    part_add_btn.click(
        fn=add_part,
        inputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
        outputs=[
            part_status_msg, part_table, part_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_chart, part_category_filter, part_edit_select, part_id,
            part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
        ],
    )

    part_load_btn.click(
        fn=load_part_for_edit,
        inputs=[part_edit_select],
        outputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status, part_status_msg],
    )

    part_update_btn.click(
        fn=update_part,
        inputs=[part_edit_select, part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
        outputs=[
            part_status_msg, part_table, part_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_chart, part_category_filter, part_edit_select, part_id,
            part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
        ],
    )

    part_delete_btn.click(
        fn=delete_part,
        inputs=[part_edit_select],
        outputs=[
            part_status_msg, part_table, part_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_chart, part_category_filter, part_edit_select, part_id,
            part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
        ],
    )

    part_clear_btn.click(
        fn=clear_part_form,
        outputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
    )

    part_filter_btn.click(
        fn=filter_parts,
        inputs=[part_search, part_category_filter, part_status_filter],
        outputs=[part_table, part_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4, part_chart],
    )

    part_reset_btn.click(
        fn=lambda: ("", "Alle", "Alle", parts_to_dataframe(), generate_part_report(), *get_part_dashboard_cards(), get_part_chart()),
        inputs=[],
        outputs=[part_search, part_category_filter, part_status_filter, part_table, part_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4, part_chart],
    )

    part_export_txt_btn.click(fn=export_parts_txt, outputs=[part_export_status])
    part_export_csv_btn.click(fn=export_parts_csv, outputs=[part_export_status])
    part_export_xlsx_btn.click(fn=export_parts_excel, outputs=[part_export_status])

    # Customers
    customer_add_btn.click(
        fn=add_customer,
        inputs=[customer_id, customer_name, customer_phone, customer_email, customer_address],
        outputs=[
            customer_status_msg, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_chart, customer_edit_select, car_customer, customer_id,
            customer_id, customer_name, customer_phone, customer_email, customer_address
        ],
    )

    customer_load_btn.click(
        fn=load_customer_for_edit,
        inputs=[customer_edit_select],
        outputs=[customer_id, customer_name, customer_phone, customer_email, customer_address, customer_status_msg],
    )

    customer_update_btn.click(
        fn=update_customer,
        inputs=[customer_edit_select, customer_id, customer_name, customer_phone, customer_email, customer_address],
        outputs=[
            customer_status_msg, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_chart, customer_edit_select, car_customer, customer_id,
            customer_id, customer_name, customer_phone, customer_email, customer_address
        ],
    )

    customer_delete_btn.click(
        fn=delete_customer,
        inputs=[customer_edit_select],
        outputs=[
            customer_status_msg, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_chart, customer_edit_select, car_customer, customer_id,
            customer_id, customer_name, customer_phone, customer_email, customer_address
        ],
    )

    customer_clear_btn.click(
        fn=clear_customer_form,
        outputs=[customer_id, customer_name, customer_phone, customer_email, customer_address],
    )

    customer_filter_btn.click(
        fn=filter_customers,
        inputs=[customer_search],
        outputs=[customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3, customer_chart],
    )

    customer_reset_btn.click(
        fn=lambda: ("", customers_to_dataframe(), generate_customer_report(), *get_customer_dashboard_cards(), get_customer_chart()),
        inputs=[],
        outputs=[customer_search, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3, customer_chart],
    )

    customer_export_txt_btn.click(fn=export_customers_txt, outputs=[customer_export_status])
    customer_export_csv_btn.click(fn=export_customers_csv, outputs=[customer_export_status])
    customer_export_xlsx_btn.click(fn=export_customers_excel, outputs=[customer_export_status])

if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Base(),
        css=custom_css,
    )