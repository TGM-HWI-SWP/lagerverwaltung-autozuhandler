from __future__ import annotations

import pandas as pd
import gradio as gr

from domain.models.car import Car
from domain.models.customer import Customer
from domain.models.part import Part
from reports.car_reports import generate_car_report
from reports.customer_reports import generate_customer_report
from reports.part_reports import generate_part_report
from services.dashboard_service import DashboardService
from services.formatting_service import (
    format_currency,
    invoice_status_badge,
    part_status_badge,
    safe_str,
)
from ui.charts import get_car_chart, get_customer_chart, get_part_chart


def kpi_card_html(title: str, value: str, icon: str, accent: str = "blue") -> str:
    return f"""
    <div class="kpi-card {accent}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-body">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
    </div>
    """


def get_customer_name_by_id(customer_id: str | None, customers: list[Customer]) -> str:
    if not customer_id:
        return "-"
    for customer in customers:
        if customer.id == customer_id:
            return customer.name
    return "-"


def cars_to_dataframe(cars: list[Car], customers: list[Customer]) -> pd.DataFrame:
    if not cars:
        return pd.DataFrame(
            columns=[
                "ID", "Marke", "Modell", "Baujahr", "Kilometer", "Kraftstoff",
                "Farbe", "Ankauf", "Verkauf", "Gewinn", "Kunde", "Verkaufsdatum",
                "Rechnungsstatus", "Status",
            ]
        )

    rows = []
    for car in cars:
        rows.append({
            "ID": car.id,
            "Marke": car.brand,
            "Modell": car.model,
            "Baujahr": car.year,
            "Kilometer": car.mileage,
            "Kraftstoff": car.fuel.value,
            "Farbe": car.color,
            "Ankauf": format_currency(car.purchase_price),
            "Verkauf": format_currency(car.sale_price),
            "Gewinn": format_currency(car.profit),
            "Kunde": get_customer_name_by_id(car.customer_id, customers),
            "Verkaufsdatum": car.sale_date,
            "Rechnungsstatus": invoice_status_badge(car.invoice_status),
            "Status": car.status.value,
        })
    return pd.DataFrame(rows)


def parts_to_dataframe(parts: list[Part]) -> pd.DataFrame:
    if not parts:
        return pd.DataFrame(
            columns=["ID", "Name", "Kategorie", "Marke", "Preis", "Bestand", "Gesamtwert", "Status"]
        )

    rows = []
    for part in parts:
        rows.append({
            "ID": part.id,
            "Name": part.name,
            "Kategorie": part.category,
            "Marke": part.brand,
            "Preis": format_currency(part.price),
            "Bestand": part.stock,
            "Gesamtwert": format_currency(part.total_value),
            "Status": part_status_badge(part.status),
        })
    return pd.DataFrame(rows)


def customers_to_dataframe(customers: list[Customer]) -> pd.DataFrame:
    if not customers:
        return pd.DataFrame(columns=["ID", "Name", "Telefon", "E-Mail", "Adresse"])

    rows = []
    for customer in customers:
        rows.append({
            "ID": customer.id,
            "Name": customer.name,
            "Telefon": customer.phone,
            "E-Mail": customer.email,
            "Adresse": customer.address,
        })
    return pd.DataFrame(rows)


def make_choice_suggestions(search_text: str, source_list: list[str]):
    text = safe_str(search_text).lower()
    if not text:
        result = source_list[:8]
    else:
        starts = [v for v in source_list if v.lower().startswith(text)]
        contains = [v for v in source_list if text in v.lower() and v not in starts]
        result = (starts + contains)[:8]
    return gr.update(choices=result, value=None)


def pick_dropdown_value(value: str | None) -> str:
    return value or ""


def customer_choices(customers: list[Customer], include_empty: bool = True) -> list[str]:
    result: list[str] = []
    if include_empty:
        result.append("-")
    result.extend(f"{customer.id} | {customer.name}" for customer in customers)
    return result


def extract_customer_id(choice: str) -> str:
    value = safe_str(choice)
    if not value or value == "-":
        return ""
    return value.split("|")[0].strip()


def car_id_choices(cars: list[Car]) -> list[str]:
    return [car.id for car in cars]


def part_id_choices(parts: list[Part]) -> list[str]:
    return [part.id for part in parts]


def customer_id_choices(customers: list[Customer]) -> list[str]:
    return [customer.id for customer in customers]


def car_dashboard_cards(stats) -> tuple[str, str, str, str, str]:
    return (
        kpi_card_html("Fahrzeuge gesamt", str(stats.total), "🚗", "blue"),
        kpi_card_html("Verfügbar", str(stats.available), "✅", "green"),
        kpi_card_html("Verkauft", str(stats.sold), "📄", "violet"),
        kpi_card_html("Gesamtgewinn", format_currency(stats.total_profit), "💰", "gold"),
        kpi_card_html("Höchster Verkauf", stats.top_sale_text, "⭐", "blue"),
    )


def part_dashboard_cards(stats) -> tuple[str, str, str, str]:
    return (
        kpi_card_html("Teile gesamt", str(stats.total), "📦", "blue"),
        kpi_card_html("Gesamtbestand", str(stats.total_stock), "📚", "green"),
        kpi_card_html("Lagerwert", format_currency(stats.total_value), "💶", "violet"),
        kpi_card_html("Wertvollstes Teil", stats.top_value_text, "🏆", "gold"),
    )


def customer_dashboard_cards(stats) -> tuple[str, str, str]:
    return (
        kpi_card_html("Kunden gesamt", str(stats.total), "👥", "blue"),
        kpi_card_html("Mit E-Mail", str(stats.with_email), "📧", "green"),
        kpi_card_html("Mit Telefon", str(stats.with_phone), "📞", "violet"),
    )


def refresh_car_view(
    cars: list[Car],
    customers: list[Customer],
    dashboard_service: DashboardService,
    brand_choices: list[str],
    next_car_id: str,
    status_message: str = "",
):
    stats = dashboard_service.get_car_stats(cars)
    return (
        status_message,
        cars_to_dataframe(cars, customers),
        generate_car_report(cars, customers) if cars else "Keine passenden Fahrzeuge gefunden.",
        *car_dashboard_cards(stats),
        get_car_chart(cars),
        gr.update(choices=["Alle"] + brand_choices, value="Alle"),
        gr.update(choices=car_id_choices(cars), value=None),
        gr.update(choices=customer_choices(customers), value="-"),
        next_car_id,
    )


def refresh_part_view(
    parts: list[Part],
    dashboard_service: DashboardService,
    category_choices: list[str],
    next_part_id: str,
    status_message: str = "",
):
    stats = dashboard_service.get_part_stats(parts)
    return (
        status_message,
        parts_to_dataframe(parts),
        generate_part_report(parts) if parts else "Keine passenden Teile gefunden.",
        *part_dashboard_cards(stats),
        get_part_chart(parts),
        gr.update(choices=["Alle"] + category_choices, value="Alle"),
        gr.update(choices=part_id_choices(parts), value=None),
        next_part_id,
    )


def refresh_customer_view(
    customers: list[Customer],
    cars: list[Car],
    dashboard_service: DashboardService,
    next_customer_id: str,
    status_message: str = "",
):
    stats = dashboard_service.get_customer_stats(customers)
    return (
        status_message,
        customers_to_dataframe(customers),
        generate_customer_report(customers) if customers else "Keine passenden Kunden gefunden.",
        *customer_dashboard_cards(stats),
        get_customer_chart(customers),
        gr.update(choices=customer_id_choices(customers), value=None),
        gr.update(choices=customer_choices(customers), value="-"),
        next_customer_id,
    )