from __future__ import annotations
 
from src.adapters.memory_repositories import InMemoryPartRepository
from src.services.part_service import PartService
 
 
def build_service() -> PartService:
    return PartService(part_repository=InMemoryPartRepository())
 
 
def test_create_part_success() -> None:
    service = build_service()
 
    result = service.create_part(
        part_id="PRT-0001",
        name="winterreifen",
        category="reifen",
        brand="michelin",
        price="199.99",
        stock="8",
        status="Verfügbar",
    )
 
    assert result.success is True
    assert result.data["part"]["name"] == "Winterreifen"
    assert result.data["part"]["category"] == "Reifen"
    assert len(service.get_all()) == 1
 
 
def test_create_part_duplicate_id_fails() -> None:
    service = build_service()
 
    service.create_part(
        part_id="PRT-0001",
        name="Bremsscheibe",
        category="Bremsen",
        brand="ATE",
        price="89.50",
        stock="4",
        status="Verfügbar",
    )
 
    result = service.create_part(
        part_id="PRT-0001",
        name="Ölfilter",
        category="Öl",
        brand="Bosch",
        price="12.99",
        stock="12",
        status="Verfügbar",
    )
 
    assert result.success is False
    assert "existiert bereits" in result.message
 
 
def test_create_part_invalid_numbers_fail() -> None:
    service = build_service()
 
    result = service.create_part(
        part_id="PRT-0001",
        name="Felge",
        category="Felgen",
        brand="BBS",
        price="abc",
        stock="3",
        status="Verfügbar",
    )
 
    assert result.success is False
    assert "Preis muss eine Zahl" in result.message
 
 
def test_update_part_success() -> None:
    service = build_service()
 
    service.create_part(
        part_id="PRT-0001",
        name="Batterie",
        category="Batterie",
        brand="Varta",
        price="119.99",
        stock="5",
        status="Verfügbar",
    )
 
    result = service.update_part(
        selected_id="PRT-0001",
        part_id="PRT-0001",
        name="Batterie Premium",
        category="Batterie",
        brand="Varta",
        price="129.99",
        stock="6",
        status="Nachbestellen",
    )
 
    assert result.success is True
    updated = service.get_by_id("PRT-0001")
    assert updated is not None
    assert updated["name"] == "Batterie Premium"
    assert updated["stock"] == 6
 
 
def test_delete_part_success() -> None:
    service = build_service()
 
    service.create_part(
        part_id="PRT-0001",
        name="LED Lampe",
        category="Licht",
        brand="Philips",
        price="24.90",
        stock="10",
        status="Verfügbar",
    )
 
    result = service.delete_part("PRT-0001")
 
    assert result.success is True
    assert service.get_by_id("PRT-0001") is None
 
 
def test_filter_parts_by_category_and_status() -> None:
    service = build_service()
 
    service.create_part(
        part_id="PRT-0001",
        name="Sommerreifen",
        category="Reifen",
        brand="Conti",
        price="149.99",
        stock="10",
        status="Verfügbar",
    )
    service.create_part(
        part_id="PRT-0002",
        name="Motoröl",
        category="Öl",
        brand="Castrol",
        price="39.99",
        stock="2",
        status="Nachbestellen",
    )
 
    filtered = service.filter_parts(search_term="", category_filter="Reifen", status_filter="Verfügbar")
 
    assert len(filtered) == 1
    assert filtered[0]["id"] == "PRT-0001"