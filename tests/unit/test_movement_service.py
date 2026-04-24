from __future__ import annotations

from src.adapters.memory_repositories import InMemoryMovementRepository
from src.services.movement_service import MovementService


def test_log_and_read_movements() -> None:
    repo = InMemoryMovementRepository()
    service = MovementService(repo)

    service.log(
        entity_type="Teil",
        entity_id="PRT-0001",
        action="Erstellt",
        description="Teil angelegt",
        quantity_delta=10,
        reference="Initialbestand",
    )

    entries = service.get_all()

    assert len(entries) == 1
    assert entries[0]["entity_type"] == "Teil"
    assert entries[0]["entity_id"] == "PRT-0001"
    assert entries[0]["action"] == "Erstellt"
    assert entries[0]["quantity_delta"] == 10


def test_filter_movements() -> None:
    repo = InMemoryMovementRepository()
    service = MovementService(repo)

    service.log("Teil", "PRT-0001", "Erstellt", "Teil angelegt", 5, "")
    service.log("Fahrzeug", "CAR-0001", "Aktualisiert", "Status geändert", 0, "")

    filtered = service.filter_movements(search_term="", entity_filter="Teil", action_filter="Alle")

    assert len(filtered) == 1
    assert filtered[0]["entity_type"] == "Teil"