from __future__ import annotations
 
from datetime import datetime
 
import pandas as pd
 
from src.ports.repositories import CarRepositoryPort, CustomerRepositoryPort
from src.services.formatting_service import calc_profit, format_currency, invoice_status_badge, safe_str
 
 
class CarReportService:
    def __init__(
        self,
        car_repository: CarRepositoryPort,
        customer_repository: CustomerRepositoryPort,
    ) -> None:
        self.car_repository = car_repository
        self.customer_repository = customer_repository
 
    def get_cars(self) -> list[dict]:
        return self.car_repository.get_all()
 
    def get_customer_name_by_id(self, customer_id: object) -> str:
        customer_id = safe_str(customer_id).upper()
        if not customer_id:
            return "-"
 
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            return "-"
        return safe_str(customer.get("name")) or "-"
 
    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:
        source = data if data is not None else self.get_cars()
 
        if not source:
            return pd.DataFrame(
                columns=[
                    "ID",
                    "Marke",
                    "Modell",
                    "Baujahr",
                    "Kilometer",
                    "Kraftstoff",
                    "Farbe",
                    "Ankauf",
                    "Verkauf",
                    "Gewinn",
                    "Kunde",
                    "Verkaufsdatum",
                    "Rechnungsstatus",
                    "Status",
                ]
            )
 
        rows: list[dict] = []
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
                "Kunde": self.get_customer_name_by_id(car.get("customer_id", "")),
                "Verkaufsdatum": car.get("sale_date", ""),
                "Rechnungsstatus": invoice_status_badge(car.get("invoice_status", "Offen")),
                "Status": car["status"],
            })
 
        return pd.DataFrame(rows)
 
    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str, str, str]:
        source = data if data is not None else self.get_cars()
 
        total = len(source)
        available = sum(1 for car in source if car["status"] == "Verfügbar")
        sold = sum(1 for car in source if car["status"] == "Verkauft")
        total_profit = sum(calc_profit(car["purchase_price"], car["sale_price"]) for car in source)
 
        if source:
            top = max(source, key=lambda x: float(x["sale_price"]))
            top_text = f"{top['brand']} {top['model']} ({float(top['sale_price']):.2f} €)"
        else:
            top_text = "-"
 
        return (
            str(total),
            str(available),
            str(sold),
            format_currency(total_profit),
            top_text,
        )
 
    def generate_text_report(self, data: list[dict] | None = None) -> str:
        source = data if data is not None else self.get_cars()
 
        if not source:
            return "Kein Fahrzeugreport möglich, da noch keine Fahrzeuge vorhanden sind."
 
        total, available, sold, total_profit, top_text = self.get_stats(source)
        reserved = sum(1 for car in source if car["status"] == "Reserviert")
 
        lines = [
            "Autozuhändler – Fahrzeugreport",
            "================================",
            f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
            "",
            f"Fahrzeuge gesamt: {total}",
            f"Verfügbar: {available}",
            f"Reserviert: {reserved}",
            f"Verkauft: {sold}",
            f"Gesamtgewinn: {total_profit}",
            f"Höchster Verkauf: {top_text}",
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
                f"Kunde: {self.get_customer_name_by_id(car.get('customer_id', ''))} | "
                f"Rechnung: {car.get('invoice_status', 'Offen')} | Status: {car['status']}"
            )
 
        return "\n".join(lines)
 
    def get_profit_statistics(self, data: list[dict] | None = None) -> dict[str, object]:
        source = data if data is not None else self.get_cars()
 
        sold_cars = [car for car in source if safe_str(car.get("status")) == "Verkauft"]
        profits = [calc_profit(car["purchase_price"], car["sale_price"]) for car in sold_cars]
 
        return {
            "sold_count": len(sold_cars),
            "total_profit": sum(profits),
            "average_profit": (sum(profits) / len(profits)) if profits else 0.0,
            "max_profit": max(profits) if profits else 0.0,
            "min_profit": min(profits) if profits else 0.0,
        }