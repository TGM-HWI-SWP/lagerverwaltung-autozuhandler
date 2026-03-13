import pandas as pd
from src.services.formatting_service import format_currency, calc_profit, part_status_badge, invoice_status_badge


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


class DashboardService:
    def __init__(self, customer_name_lookup):
        self.customer_name_lookup = customer_name_lookup

    def cars_to_dataframe(self, data):
        if not data:
            return pd.DataFrame(
                columns=[
                    "ID", "Marke", "Modell", "Baujahr", "Kilometer", "Kraftstoff",
                    "Farbe", "Ankauf", "Verkauf", "Gewinn", "Kunde", "Verkaufsdatum",
                    "Rechnungsstatus", "Status"
                ]
            )

        rows = []
        for car in data:
            rows.append({
                "ID": car.id,
                "Marke": car.brand,
                "Modell": car.model,
                "Baujahr": car.year,
                "Kilometer": car.mileage,
                "Kraftstoff": car.fuel,
                "Farbe": car.color,
                "Ankauf": format_currency(car.purchase_price),
                "Verkauf": format_currency(car.sale_price),
                "Gewinn": format_currency(calc_profit(car.purchase_price, car.sale_price)),
                "Kunde": self.customer_name_lookup(car.customer_id),
                "Verkaufsdatum": car.sale_date,
                "Rechnungsstatus": invoice_status_badge(car.invoice_status),
                "Status": car.status,
            })
        return pd.DataFrame(rows)

    def parts_to_dataframe(self, data):
        if not data:
            return pd.DataFrame(
                columns=["ID", "Name", "Kategorie", "Marke", "Preis", "Bestand", "Gesamtwert", "Status"]
            )

        rows = []
        for part in data:
            rows.append({
                "ID": part.id,
                "Name": part.name,
                "Kategorie": part.category,
                "Marke": part.brand,
                "Preis": format_currency(part.price),
                "Bestand": part.stock,
                "Gesamtwert": format_currency(part.price * part.stock),
                "Status": part_status_badge(part.status),
            })
        return pd.DataFrame(rows)

    def customers_to_dataframe(self, data):
        if not data:
            return pd.DataFrame(columns=["ID", "Name", "Telefon", "E-Mail", "Adresse"])

        rows = []
        for customer in data:
            rows.append({
                "ID": customer.id,
                "Name": customer.name,
                "Telefon": customer.phone,
                "E-Mail": customer.email,
                "Adresse": customer.address,
            })
        return pd.DataFrame(rows)

    def get_car_dashboard_cards(self, data):
        total = len(data)
        available = sum(1 for car in data if car.status == "Verfügbar")
        sold = sum(1 for car in data if car.status == "Verkauft")
        total_profit = sum(calc_profit(car.purchase_price, car.sale_price) for car in data)

        if data:
            top = max(data, key=lambda x: x.sale_price)
            top_text = f"{top.brand} {top.model} ({top.sale_price:.2f} €)"
        else:
            top_text = "-"

        return (
            kpi_card_html("Fahrzeuge gesamt", str(total), "🚗", "blue"),
            kpi_card_html("Verfügbar", str(available), "✅", "green"),
            kpi_card_html("Verkauft", str(sold), "📄", "violet"),
            kpi_card_html("Gesamtgewinn", format_currency(total_profit), "💰", "gold"),
            kpi_card_html("Höchster Verkauf", top_text, "⭐", "blue"),
        )

    def get_part_dashboard_cards(self, data):
        total = len(data)
        stock = sum(int(part.stock) for part in data)
        total_value = sum(float(part.price) * int(part.stock) for part in data)

        if data:
            top = max(data, key=lambda x: float(x.price) * int(x.stock))
            top_text = f"{top.name} ({format_currency(float(top.price) * int(top.stock))})"
        else:
            top_text = "-"

        return (
            kpi_card_html("Teile gesamt", str(total), "📦", "blue"),
            kpi_card_html("Gesamtbestand", str(stock), "📚", "green"),
            kpi_card_html("Lagerwert", format_currency(total_value), "💶", "violet"),
            kpi_card_html("Wertvollstes Teil", top_text, "🏆", "gold"),
        )

    def get_customer_dashboard_cards(self, data):
        total = len(data)
        with_email = sum(1 for customer in data if str(customer.email).strip())
        with_phone = sum(1 for customer in data if str(customer.phone).strip())

        return (
            kpi_card_html("Kunden gesamt", str(total), "👥", "blue"),
            kpi_card_html("Mit E-Mail", str(with_email), "📧", "green"),
            kpi_card_html("Mit Telefon", str(with_phone), "📞", "violet"),
        )