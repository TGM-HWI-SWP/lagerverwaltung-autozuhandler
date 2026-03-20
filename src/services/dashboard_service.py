from __future__ import annotations
 
 
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
 
 
class DashboardService:

    def get_car_dashboard_cards(

        self,

        total: str,

        available: str,

        sold: str,

        total_profit: str,

        top_text: str,

    ) -> tuple[str, str, str, str, str]:

        return (

            kpi_card_html("Fahrzeuge gesamt", total, "🚗", "blue"),

            kpi_card_html("Verfügbar", available, "✅", "green"),

            kpi_card_html("Verkauft", sold, "📄", "violet"),

            kpi_card_html("Gesamtgewinn", total_profit, "💰", "gold"),

            kpi_card_html("Höchster Verkauf", top_text, "⭐", "blue"),

        )
 
    def get_part_dashboard_cards(

        self,

        total: str,

        stock: str,

        total_value: str,

        top: str,

    ) -> tuple[str, str, str, str]:

        return (

            kpi_card_html("Teile gesamt", total, "📦", "blue"),

            kpi_card_html("Gesamtbestand", stock, "📚", "green"),

            kpi_card_html("Lagerwert", total_value, "💶", "violet"),

            kpi_card_html("Wertvollstes Teil", top, "🏆", "gold"),

        )
 
    def get_customer_dashboard_cards(

        self,

        total: str,

        with_email: str,

        with_phone: str,

    ) -> tuple[str, str, str]:

        return (

            kpi_card_html("Kunden gesamt", total, "👥", "blue"),

            kpi_card_html("Mit E-Mail", with_email, "📧", "green"),

            kpi_card_html("Mit Telefon", with_phone, "📞", "violet"),

        )
 