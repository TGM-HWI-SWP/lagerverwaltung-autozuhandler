from __future__ import annotations

from src.adapters.memory_repositories import InMemoryMovementRepository
from src.reports.movement_reports import MovementReportService


def test_movement_report_dataframe_empty() -> None:
    report = MovementReportService(InMemoryMovementRepository())
    df = report.generate_dataframe()

    assert df.empty is True
    assert "Zeitpunkt" in df.columns
    assert "Aktion" in df.columns


def test_movement_report_stats() -> None:
    repo = InMemoryMovementRepository()
    repo.add({
        "timestamp": "01.01.2026 10:00:00",
        "entity_type": "Teil",
        "entity_id": "PRT-0001",
        "action": "Erstellt",
        "description": "Teil angelegt",
        "quantity_delta": 4,
        "reference": "",
    })
    repo.add({
        "timestamp": "01.01.2026 10:05:00",
        "entity_type": "Teil",
        "entity_id": "PRT-0001",
        "action": "Aktualisiert",
        "description": "Bestand geändert",
        "quantity_delta": 2,
        "reference": "",
    })

    report = MovementReportService(repo)
    total, created, updated, deleted = report.get_stats()

    assert total == "2"
    assert created == "1"
    assert updated == "1"
    assert deleted == "0"


def test_movement_report_text_contains_data() -> None:
    repo = InMemoryMovementRepository()
    repo.add({
        "timestamp": "01.01.2026 10:00:00",
        "entity_type": "Kunde",
        "entity_id": "KUN-0001",
        "action": "Erstellt",
        "description": "Kunde angelegt",
        "quantity_delta": 0,
        "reference": "",
    })

    report = MovementReportService(repo)
    text = report.generate_text_report()

    assert "Movement-Report" in text
    assert "KUN-0001" in text
    assert "Kunde angelegt" in text