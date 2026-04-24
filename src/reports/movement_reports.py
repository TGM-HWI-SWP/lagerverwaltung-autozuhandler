from __future__ import annotations

from datetime import datetime

import pandas as pd

from src.ports.repositories import MovementRepositoryPort
from src.services.formatting_service import safe_str


class MovementReportService:
    def __init__(self, movement_repository: MovementRepositoryPort) -> None:
        self.movement_repository = movement_repository

    def get_movements(self) -> list[dict]:
        return self.movement_repository.get_all()

    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:
        source = data if data is not None else self.get_movements()

        if not source:
            return pd.DataFrame(
                columns=[
                    "Zeitpunkt",
                    "Typ",
                    "Objekt-ID",
                    "Aktion",
                    "Menge Δ",
                    "Beschreibung",
                    "Referenz",
                ]
            )

        rows: list[dict] = []
        for entry in source:
            rows.append({
                "Zeitpunkt": entry["timestamp"],
                "Typ": entry["entity_type"],
                "Objekt-ID": entry["entity_id"],
                "Aktion": entry["action"],
                "Menge Δ": entry["quantity_delta"],
                "Beschreibung": entry["description"],
                "Referenz": entry.get("reference", ""),
            })

        return pd.DataFrame(rows)

    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str, str]:
        source = data if data is not None else self.get_movements()

        total = len(source)
        created = sum(1 for entry in source if safe_str(entry.get("action")) == "Erstellt")
        updated = sum(1 for entry in source if safe_str(entry.get("action")) == "Aktualisiert")
        deleted = sum(1 for entry in source if safe_str(entry.get("action")) == "Gelöscht")

        return str(total), str(created), str(updated), str(deleted)

    def generate_text_report(self, data: list[dict] | None = None) -> str:
        source = data if data is not None else self.get_movements()

        if not source:
            return "Kein Movement-Report möglich, da noch keine Bewegungen vorhanden sind."

        total, created, updated, deleted = self.get_stats(source)

        lines = [
            "Autozuhändler – Movement-Report",
            "===============================",
            f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
            "",
            f"Bewegungen gesamt: {total}",
            f"Erstellt: {created}",
            f"Aktualisiert: {updated}",
            f"Gelöscht: {deleted}",
            "",
            "Bewegungsliste:",
        ]

        for entry in source:
            lines.append(
                f"- {entry['timestamp']} | {entry['entity_type']} | {entry['entity_id']} | "
                f"{entry['action']} | Menge Δ: {entry['quantity_delta']} | "
                f"{entry['description']} | Ref: {entry.get('reference', '')}"
            )

        return "\n".join(lines)