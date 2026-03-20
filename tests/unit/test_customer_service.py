from __future__ import annotations
 
from src.adapters.memory_repositories import InMemoryCarRepository, InMemoryCustomerRepository
from src.services.customer_service import CustomerService
 
 
def build_service(
    customer_repository: InMemoryCustomerRepository | None = None,
    car_repository: InMemoryCarRepository | None = None,
) -> CustomerService:
    return CustomerService(
        customer_repository=customer_repository or InMemoryCustomerRepository(),
        car_repository=car_repository or InMemoryCarRepository(),
    )
 
 
def test_create_customer_success() -> None:
    service = build_service()
 
    result = service.create_customer(
        customer_id="KUN-0001",
        name="max mustermann",
        phone="06641234567",
        email="max@example.com",
        address="wien teststraße 1",
    )
 
    assert result.success is True
    assert result.data["customer"]["name"] == "Max Mustermann"
    assert len(service.get_all()) == 1
 
 
def test_create_customer_requires_name() -> None:
    service = build_service()
 
    result = service.create_customer(
        customer_id="KUN-0001",
        name="",
        phone="",
        email="",
        address="",
    )
 
    assert result.success is False
    assert "Kundennamen" in result.message
 
 
def test_update_customer_success() -> None:
    service = build_service()
 
    service.create_customer(
        customer_id="KUN-0001",
        name="anna meier",
        phone="111",
        email="anna@example.com",
        address="graz",
    )
 
    result = service.update_customer(
        selected_id="KUN-0001",
        customer_id="KUN-0001",
        name="anna meier-neu",
        phone="222",
        email="anna.neu@example.com",
        address="linz",
    )
 
    assert result.success is True
    updated = service.get_by_id("KUN-0001")
    assert updated is not None
    assert updated["name"] == "Anna Meier-neu"
    assert updated["phone"] == "222"
 
 
def test_delete_customer_fails_when_linked_to_car() -> None:
    customer_repository = InMemoryCustomerRepository()
    car_repository = InMemoryCarRepository()
 
    customer_repository.add({
        "id": "KUN-0001",
        "name": "Max Kunde",
        "phone": "",
        "email": "",
        "address": "",
    })
    car_repository.add({
        "id": "CAR-0001",
        "brand": "Audi",
        "model": "A4",
        "year": 2020,
        "mileage": 10000,
        "fuel": "Benzin",
        "color": "Schwarz",
        "purchase_price": 20000.0,
        "sale_price": 24000.0,
        "customer_id": "KUN-0001",
        "sale_date": "",
        "invoice_status": "Offen",
        "status": "Reserviert",
    })
 
    service = build_service(
        customer_repository=customer_repository,
        car_repository=car_repository,
    )
 
    result = service.delete_customer("KUN-0001")
 
    assert result.success is False
    assert "verknüpft" in result.message
 
 
def test_delete_customer_success() -> None:
    service = build_service()
 
    service.create_customer(
        customer_id="KUN-0001",
        name="Lena Test",
        phone="123",
        email="lena@example.com",
        address="Salzburg",
    )
 
    result = service.delete_customer("KUN-0001")
 
    assert result.success is True
    assert service.get_by_id("KUN-0001") is None
 
 
def test_filter_customers_by_term() -> None:
    service = build_service()
 
    service.create_customer(
        customer_id="KUN-0001",
        name="Julia Moser",
        phone="111",
        email="julia@example.com",
        address="Wien",
    )
    service.create_customer(
        customer_id="KUN-0002",
        name="Paul Gruber",
        phone="222",
        email="paul@example.com",
        address="Linz",
    )
 
    filtered = service.filter_customers("julia")
 
    assert len(filtered) == 1
    assert filtered[0]["id"] == "KUN-0001"