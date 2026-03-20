from __future__ import annotations
 
from src.adapters.memory_repositories import InMemoryCarRepository, InMemoryCustomerRepository, InMemoryPartRepository

from src.reports.car_reports import CarReportService

from src.reports.inventory_report import InventoryReportService

from src.services.car_service import CarService

from src.services.customer_service import CustomerService

from src.services.part_service import PartService
 
 
def test_car_service_rejects_negative_price() -> None:

    service = CarService(

        car_repository=InMemoryCarRepository(),

        customer_repository=InMemoryCustomerRepository(),

    )
 
    result = service.create_car(

        car_id="CAR-0001",

        brand="Audi",

        model="A3",

        year="2020",

        mileage="10000",

        fuel="Benzin",

        color="Schwarz",

        purchase_price="-1",

        sale_price="10000",

        customer_id="",

        invoice_status="Offen",

        status="Verfügbar",

    )
 
    assert result.success is False

    assert "dürfen nicht negativ" in result.message
 
 
def test_part_service_rejects_negative_stock() -> None:

    service = PartService(part_repository=InMemoryPartRepository())
 
    result = service.create_part(

        part_id="PRT-0001",

        name="Ölfilter",

        category="Öl",

        brand="Bosch",

        price="10",

        stock="-2",

        status="Verfügbar",

    )
 
    assert result.success is False

    assert "gültige Werte" in result.message
 
 
def test_customer_service_rejects_missing_name() -> None:

    service = CustomerService(

        customer_repository=InMemoryCustomerRepository(),

        car_repository=InMemoryCarRepository(),

    )
 
    result = service.create_customer(

        customer_id="KUN-0001",

        name="",

        phone="",

        email="",

        address="",

    )
 
    assert result.success is False

    assert "Kundennamen" in result.message
 
 
def test_inventory_report_handles_empty_repo() -> None:

    report = InventoryReportService(part_repository=InMemoryPartRepository())

    stats = report.get_stats()
 
    assert stats[0] == "0"

    assert stats[1] == "0"

    assert stats[2] == "0.00 €"

    assert stats[3] == "-"
 
 
def test_car_report_handles_unknown_customer() -> None:

    car_repo = InMemoryCarRepository()

    customer_repo = InMemoryCustomerRepository()
 
    car_repo.add({

        "id": "CAR-0001",

        "brand": "BMW",

        "model": "320d",

        "year": 2019,

        "mileage": 55000,

        "fuel": "Diesel",

        "color": "Grau",

        "purchase_price": 14000.0,

        "sale_price": 18000.0,

        "customer_id": "KUN-9999",

        "sale_date": "",

        "invoice_status": "Offen",

        "status": "Reserviert",

    })
 
    report = CarReportService(car_repository=car_repo, customer_repository=customer_repo)

    df = report.generate_dataframe()
 
    assert df.iloc[0]["Kunde"] == "-"
 