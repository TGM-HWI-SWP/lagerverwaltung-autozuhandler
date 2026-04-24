from __future__ import annotations

from datetime import datetime

from src.ports.repositories import MovementRepositoryPort
from src.services.formatting_service import safe_str


class MovementService:
    def __init__(self, movement_repository: MovementRepositoryPort) -> None:
        self.movement_repository = movement_repository

    def log(
        self,
        entity_type: object,
        entity_id: object,
        action: object,
        description: object,
        quantity_delta: object = 0,
        reference: object = "",
    ) -> None:
        entry = {
            "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "entity_type": safe_str(entity_type),
            "entity_id": safe_str(entity_id).upper(),
            "action": safe_str(action),
            "description": safe_str(description),
            "quantity_delta": self._to_int(quantity_delta),
            "reference": safe_str(reference),
        }
        self.movement_repository.add(entry)

    def get_all(self) -> list[dict]:
        return self.movement_repository.get_all()

    def filter_movements(
        self,
        search_term: object = "",
        entity_filter: object = "Alle",
        action_filter: object = "Alle",
    ) -> list[dict]:
        entries = self.movement_repository.get_all()

        term = safe_str(search_term).lower()
        prepared_entity_filter = safe_str(entity_filter)
        prepared_action_filter = safe_str(action_filter)

        if term:
            entries = [
                entry
                for entry in entries
                if term in safe_str(entry.get("timestamp")).lower()
                or term in safe_str(entry.get("entity_type")).lower()
                or term in safe_str(entry.get("entity_id")).lower()
                or term in safe_str(entry.get("action")).lower()
                or term in safe_str(entry.get("description")).lower()
                or term in safe_str(entry.get("reference")).lower()
            ]

        if prepared_entity_filter and prepared_entity_filter != "Alle":
            entries = [
                entry for entry in entries
                if safe_str(entry.get("entity_type")) == prepared_entity_filter
            ]

        if prepared_action_filter and prepared_action_filter != "Alle":
            entries = [
                entry for entry in entries
                if safe_str(entry.get("action")) == prepared_action_filter
            ]

        return entries

    def get_entity_choices(self) -> list[str]:
        values = {safe_str(entry.get("entity_type")) for entry in self.get_all() if safe_str(entry.get("entity_type"))}
        return sorted(values, key=lambda x: x.lower())

    def get_action_choices(self) -> list[str]:
        values = {safe_str(entry.get("action")) for entry in self.get_all() if safe_str(entry.get("action"))}
        return sorted(values, key=lambda x: x.lower())

    def _to_int(self, value: object) -> int:
        try:
            return int(value)
        except Exception:
            return 0