from __future__ import annotations

from datetime import datetime

from domain.models.car import Car
from domain.models.customer import Customer
from services.formatting_service import format_currency


def calc_profit(purchase_price: float, sale_price: float) -> float:
    try:
        return float(sale_price) - float(purchase_price)
    except (TypeError, ValueError):
        return 0.0


def get_customer_name_by_id(customer_id: str | None, customers: list[Customer]) -> str:
    if not customer_id:
        return "-"

    for customer in customers:
        if customer.id == customer_id:
            return customer.name
    return "-"


def generate_car_report(cars: list[Car], customers: list[Customer]) -> str:
    if not cars:
        return "Kein Fahrzeugreport möglich, da noch keine Fahrzeuge vorhanden sind."

    total = len(cars)
    available = sum(1 for car in cars if car.status.value == "Verfügbar")
    reserved = sum(1 for car in cars if car.status.value == "Reserviert")
    sold = sum(1 for car in cars if car.status.value == "Verkauft")
    total_profit = sum(calc_profit(car.purchase_price, car.sale_price) for car in cars)

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

    for car in cars:
        lines.append(
            f"- {car.id} | {car.brand} {car.model} | Baujahr {car.year} | "
            f"{car.mileage} km | {car.fuel.value} | {car.color} | "
            f"Ankauf: {format_currency(car.purchase_price)} | "
            f"Verkauf: {format_currency(car.sale_price)} | "
            f"Gewinn: {format_currency(calc_profit(car.purchase_price, car.sale_price))} | "
            f"Kunde: {get_customer_name_by_id(car.customer_id, customers)} | "
            f"Rechnung: {car.invoice_status.value} | Status: {car.status.value}"
        )

    return "\n".join(lines)