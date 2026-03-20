from __future__ import annotations
 
from src.adapters.memory_repositories import InMemoryPartRepository

from src.reports.part_reports import PartReportService
 
 
def test_part_report_empty_dataframe() -> None:

    report = PartReportService(part_repository=InMemoryPartRepository())

    df = report.generate_dataframe()
 
    assert df.empty is True

    assert "Gesamtwert" in df.columns
 
 
def test_part_report_stats() -> None:

    repo = InMemoryPartRepository()

    repo.add({

        "id": "PRT-0001",

        "name": "Batterie",

        "category": "Batterie",

        "brand": "Varta",

        "price": 100.0,

        "stock": 5,

        "status": "Verfügbar",

    })
 
    report = PartReportService(part_repository=repo)

    total, stock, total_value, top = report.get_stats()
 
    assert total == "1"

    assert stock == "5"

    assert total_value == "500.00 €"

    assert "Batterie" in top
 
 
def test_part_report_text_contains_values() -> None:

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
 
    report = PartReportService(part_repository=repo)

    text = report.generate_text_report()
 
    assert "Teile-Report" in text

    assert "Felge" in text

    assert "400.00 €" in text
 