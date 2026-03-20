from __future__ import annotations
 
from src.services.dashboard_service import DashboardService
 
 
def test_car_dashboard_cards_contain_titles() -> None:

    service = DashboardService()

    cards = service.get_car_dashboard_cards("10", "4", "3", "12000.00 €", "BMW X5")
 
    assert len(cards) == 5

    assert "Fahrzeuge gesamt" in cards[0]

    assert "Gesamtgewinn" in cards[3]
 
 
def test_part_dashboard_cards_contain_titles() -> None:

    service = DashboardService()

    cards = service.get_part_dashboard_cards("8", "25", "5000.00 €", "Felge")
 
    assert len(cards) == 4

    assert "Teile gesamt" in cards[0]

    assert "Wertvollstes Teil" in cards[3]
 
 
def test_customer_dashboard_cards_contain_titles() -> None:

    service = DashboardService()

    cards = service.get_customer_dashboard_cards("7", "5", "6")
 
    assert len(cards) == 3

    assert "Kunden gesamt" in cards[0]

    assert "Mit Telefon" in cards[2]
 