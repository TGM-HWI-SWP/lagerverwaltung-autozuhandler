from __future__ import annotations

from src.adapters.memory_repositories import InMemoryCarRepository, InMemoryCustomerRepository
from src.services.car_service import CarService
 

def build_service() -> CarService:
    return CarService(
        car_repository=InMemoryCarRepository(),
        customer_repository=InMemoryCustomerRepository(),
    )
 
 
def test_create_car_success() -> None:
    service = build_service()
 
    result = service.create_car(
        car_id="CAR-0001",
        brand="bmw",
        model="x5",
        year="2020",
        mileage="50000",
        fuel="Diesel",
        color="schwarz",
        purchase_price="22000",
        sale_price="27000",
        customer_id="",
        invoice_status="Offen",
        status="Verfügbar",
    )
 
    assert result.success is True
    assert result.data["car"]["brand"] == "BMW"
    assert result.data["car"]["model"] == "X5"
    assert len(service.get_all()) == 1


def test_create_car_duplicate_id_fails() -> None:
    service = build_service()
 
    service.create_car(
        car_id="CAR-0001",
        brand="Audi",
        model="A4",
        year="2019",
        mileage="40000",
        fuel="Benzin",
        color="rot",
        purchase_price="15000",
        sale_price="18000",
        customer_id="",
        invoice_status="Offen",
        status="Verfügbar",
    )
 
    result = service.create_car(
        car_id="CAR-0001",
        brand="BMW",
        model="320d",
        year="2020",
        mileage="30000",
        fuel="Diesel",
        color="blau",
        purchase_price="17000",
        sale_price="21000",
        customer_id="",
        invoice_status="Offen",
        status="Verfügbar",
    )
 
    assert result.success is False
    assert "existiert bereits" in result.message
 
 
def test_create_car_invalid_numeric_values_fail() -> None:
    service = build_service()
 
    result = service.create_car(
        car_id="CAR-0001",
        brand="Audi",
        model="A3",
        year="abc",
        mileage="10000",
        fuel="Benzin",
        color="weiß",
        purchase_price="10000",
        sale_price="12000",
        customer_id="",
        invoice_status="Offen",
        status="Verfügbar",
    )
 
    assert result.success is False
    assert "müssen ganze Zahlen sein" in result.message
 
 
def test_update_car_success() -> None:
    service = build_service()
 
    service.create_car(
        car_id="CAR-0001",
        brand="Audi",
        model="A3",
        year="2018",
        mileage="80000",
        fuel="Benzin",
        color="weiß",
        purchase_price="12000",
        sale_price="14500",
        customer_id="",
        invoice_status="Offen",
        status="Verfügbar",
    )
 
    result = service.update_car(
        selected_id="CAR-0001",
        car_id="CAR-0001",
        brand="Audi",
        model="A3 Sportback",
        year="2018",
        mileage="79000",
        fuel="Benzin",
        color="schwarz",
        purchase_price="12000",
        sale_price="15000",
        customer_id="",
        invoice_status="Bezahlt",
        status="Verkauft",
    )
 
    assert result.success is True
    updated = service.get_by_id("CAR-0001")
    assert updated is not None
    assert updated["model"] == "A3 Sportback"
    assert updated["status"] == "Verkauft"
    assert updated["sale_date"] != ""
 
 
def test_delete_car_success() -> None:
    service = build_service()
 
    service.create_car(
        car_id="CAR-0001",
        brand="Tesla",
        model="Model 3",
        year="2022",
        mileage="10000",
        fuel="Elektro",
        color="weiß",
        purchase_price="32000",
        sale_price="37000",
        customer_id="",
        invoice_status="Offen",
        status="Verfügbar",
    )
 
    result = service.delete_car("CAR-0001")
 
    assert result.success is True
    assert service.get_by_id("CAR-0001") is None
 
 
def test_filter_cars_by_brand_and_status() -> None:
    service = build_service()
 
    service.create_car(
        car_id="CAR-0001",
        brand="BMW",
        model="X1",
        year="2020",
        mileage="20000",
        fuel="Diesel",
        color="grau",
        purchase_price="22000",
        sale_price="26000",
        customer_id="",
        invoice_status="Offen",
        status="Verfügbar",
    )
    service.create_car(
        car_id="CAR-0002",
        brand="Audi",
        model="A4",
        year="2019",
        mileage="30000",
        fuel="Benzin",
        color="schwarz",
        purchase_price="18000",
        sale_price="22000",
        customer_id="",
        invoice_status="Offen",
        status="Verkauft",
    )
 
    filtered = service.filter_cars(search_term="", brand_filter="BMW", status_filter="Verfügbar")
 
    assert len(filtered) == 1
    assert filtered[0]["id"] == "CAR-0001"