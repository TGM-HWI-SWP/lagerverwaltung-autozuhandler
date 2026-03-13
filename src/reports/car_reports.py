from datetime import datetime
from src.services.formatting_service import format_currency, calc_profit


class CarReport:
    def __init__(self, customer_name_lookup):
        self.customer_name_lookup = customer_name_lookup

    def build_text(self, cars):
        if not cars:
            return "Kein Fahrzeugreport möglich, da noch keine Fahrzeuge vorhanden sind."

        total = len(cars)
        available = sum(1 for car in cars if car.status == "Verfügbar")
        reserved = sum(1 for car in cars if car.status == "Reserviert")
        sold = sum(1 for car in cars if car.status == "Verkauft")
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
                f"{car.mileage} km | {car.fuel} | {car.color} | "
                f"Ankauf: {format_currency(car.purchase_price)} | "
                f"Verkauf: {format_currency(car.sale_price)} | "
                f"Gewinn: {format_currency(calc_profit(car.purchase_price, car.sale_price))} | "
                f"Kunde: {self.customer_name_lookup(car.customer_id)} | "
                f"Rechnung: {car.invoice_status} | Status: {car.status}"
            )

        return "\n".join(lines)