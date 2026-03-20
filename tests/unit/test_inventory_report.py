from __future__ import annotations
 
from src.adapters.memory_repositories import InMemoryPartRepository
from src.reports.inventory_report import InventoryReportService
 
 
def build_report() -> InventoryReportService:
    repo = InMemoryPartRepository()
    return InventoryReportService(part_repository=repo)
 
 
def test_inventory_report_empty_dataframe() -> None:
    report = build_report()
    df = report.generate_dataframe()
 
    assert df.empty is True
    assert list(df.columns) == [
        "ID",
        "Name",
        "Kategorie",
        "Marke",
        "Preis",
        "Bestand",
        "Gesamtwert",
        "Status",
    ]
 
 
def test_inventory_report_stats() -> None:
    repo = InMemoryPartRepository()
    repo.add({
        "id": "PRT-0001",
        "name": "Bremsscheibe",
        "category": "Bremsen",
        "brand": "ATE",
        "price": 50.0,
        "stock": 4,
        "status": "Verfügbar",
    })
    repo.add({
        "id": "PRT-0002",
        "name": "Motoröl",
        "category": "Öl",
        "brand": "Castrol",
        "price": 20.0,
        "stock": 10,
        "status": "Nachbestellen",
    })
 
    report = InventoryReportService(part_repository=repo)
    total_parts, total_stock, total_value, top_text = report.get_stats()
 
    assert total_parts == "2"
    assert total_stock == "14"
    assert total_value == "400.00 €"
    assert "Bremsscheibe" in top_text or "Motoröl" in top_text
 
 
def test_inventory_report_text_contains_key_values() -> None:
    repo = InMemoryPartRepository()
    repo.add({
        "id": "PRT-0001",
        "name": "Winterreifen",
        "category": "Reifen",
        "brand": "Michelin",
        "price": 100.0,
        "stock": 6,
        "status": "Verfügbar",
    })
 
    report = InventoryReportService(part_repository=repo)
    text = report.generate_text_report()
 
    assert "Lagerstandsreport" in text
    assert "Winterreifen" in text
    assert "600.00 €" in text
 
 
def test_inventory_report_filter_for_report() -> None:
    repo = InMemoryPartRepository()
    repo.add({
        "id": "PRT-0001",
        "name": "Felge",
        "category": "Felgen",
        "brand": "BBS",
        "price": 200.0,
        "stock": 2,
        "status": "Verfügbar",
    })
    repo.add({
        "id": "PRT-0002",
        "name": "Ölfilter",
        "category": "Öl",
        "brand": "Bosch",
        "price": 15.0,
        "stock": 5,
        "status": "Nachbestellen",
    })
 
    report = InventoryReportService(part_repository=repo)
    filtered = report.filter_for_report(
        search_term="",
        category_filter="Felgen",
        status_filter="Verfügbar",
    )
 
    assert len(filtered) == 1
    assert filtered[0]["id"] == "PRT-0001"