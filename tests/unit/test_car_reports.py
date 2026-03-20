from __future__ import annotations
 
from src.adapters.memory_repositories import InMemoryCarRepository, InMemoryCustomerRepository

from src.reports.car_reports import CarReportService
 
 
def build_report() -> CarReportService:

    car_repo = InMemoryCarRepository()

    customer_repo = InMemoryCustomerRepository()

    return CarReportService(car_repository=car_repo, customer_repository=customer_repo)
 
 
def test_car_report_empty_dataframe() -> None:

    report = build_report()

    df = report.generate_dataframe()
 
    assert df.empty is True

    assert "ID" in df.columns

    assert "Gewinn" in df.columns
 
 
def test_car_report_stats() -> None:

    car_repo = InMemoryCarRepository()

    customer_repo = InMemoryCustomerRepository()
 
    car_repo.add({

        "id": "CAR-0001",

        "brand": "BMW",

        "model": "X3",

        "year": 2020,

        "mileage": 50000,

        "fuel": "Diesel",

        "color": "Schwarz",

        "purchase_price": 20000.0,

        "sale_price": 26000.0,

        "customer_id": "",

        "sale_date": "01.01.2026",

        "invoice_status": "Bezahlt",

        "status": "Verkauft",

    })
 
    report = CarReportService(car_repository=car_repo, customer_repository=customer_repo)

    total, available, sold, total_profit, top_text = report.get_stats()
 
    assert total == "1"

    assert available == "0"

    assert sold == "1"

    assert total_profit == "6000.00 €"

    assert "BMW X3" in top_text
 
 
def test_car_report_text_contains_values() -> None:

    car_repo = InMemoryCarRepository()

    customer_repo = InMemoryCustomerRepository()
 
    customer_repo.add({

        "id": "KUN-0001",

        "name": "Max Kunde",

        "phone": "",

        "email": "",

        "address": "",

    })
 
    car_repo.add({

        "id": "CAR-0001",

        "brand": "Audi",

        "model": "A4",

        "year": 2019,

        "mileage": 60000,

        "fuel": "Benzin",

        "color": "Blau",

        "purchase_price": 15000.0,

        "sale_price": 19000.0,

        "customer_id": "KUN-0001",

        "sale_date": "02.02.2026",

        "invoice_status": "Offen",

        "status": "Verkauft",

    })
 
    report = CarReportService(car_repository=car_repo, customer_repository=customer_repo)

    text = report.generate_text_report()
 
    assert "Fahrzeugreport" in text

    assert "Audi A4" in text

    assert "Max Kunde" in text
 
 
def test_car_profit_statistics() -> None:

    car_repo = InMemoryCarRepository()

    customer_repo = InMemoryCustomerRepository()
 
    car_repo.add({

        "id": "CAR-0001",

        "brand": "VW",

        "model": "Golf",

        "year": 2018,

        "mileage": 70000,

        "fuel": "Benzin",

        "color": "Weiß",

        "purchase_price": 10000.0,

        "sale_price": 13000.0,

        "customer_id": "",

        "sale_date": "03.03.2026",

        "invoice_status": "Bezahlt",

        "status": "Verkauft",

    })
 
    report = CarReportService(car_repository=car_repo, customer_repository=customer_repo)

    stats = report.get_profit_statistics()
 
    assert stats["sold_count"] == 1

    assert stats["total_profit"] == 3000.0

    assert stats["average_profit"] == 3000.0
 