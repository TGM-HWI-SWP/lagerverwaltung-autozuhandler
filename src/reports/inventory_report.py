from __future__ import annotations
 
from datetime import datetime
 
import pandas as pd
 
from src.ports.repositories import PartRepositoryPort
from src.services.formatting_service import format_currency, part_status_badge, safe_str
 
 
class InventoryReportService:
    def __init__(self, part_repository: PartRepositoryPort) -> None:
        self.part_repository = part_repository
 
    def get_parts(self) -> list[dict]:
        return self.part_repository.get_all()
 
    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:
        source = data if data is not None else self.get_parts()
 
        if not source:
            return pd.DataFrame(
                columns=[
                    "ID",
                    "Name",
                    "Kategorie",
                    "Marke",
                    "Preis",
                    "Bestand",
                    "Gesamtwert",
                    "Status",
                ]
            )
 
        rows: list[dict] = []
        for part in source:
            price = float(part["price"])
            stock = int(part["stock"])
            rows.append({
                "ID": part["id"],
                "Name": part["name"],
                "Kategorie": part["category"],
                "Marke": part["brand"],
                "Preis": format_currency(price),
                "Bestand": stock,
                "Gesamtwert": format_currency(price * stock),
                "Status": part_status_badge(part["status"]),
            })
 
        return pd.DataFrame(rows)
 
    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str, str]:
        source = data if data is not None else self.get_parts()
 
        total_parts = len(source)
        total_stock = sum(int(part["stock"]) for part in source)
        total_value = sum(float(part["price"]) * int(part["stock"]) for part in source)
 
        if source:
            top = max(source, key=lambda x: float(x["price"]) * int(x["stock"]))
            top_text = f"{top['name']} ({format_currency(float(top['price']) * int(top['stock']))})"
        else:
            top_text = "-"
 
        return (
            str(total_parts),
            str(total_stock),
            format_currency(total_value),
            top_text,
        )
 
    def generate_text_report(self, data: list[dict] | None = None) -> str:
        source = data if data is not None else self.get_parts()
 
        if not source:
            return "Kein Lagerstandsreport möglich, da noch keine Teile vorhanden sind."
 
        total_parts, total_stock, total_value, top_text = self.get_stats(source)
 
        lines = [
            "Autozuhändler – Lagerstandsreport",
            "=================================",
            f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
            "",
            f"Teile gesamt: {total_parts}",
            f"Gesamtstückzahl Lager: {total_stock}",
            f"Gesamtwert Teilelager: {total_value}",
            f"Wertvollste Position: {top_text}",
            "",
            "Lagerbestand:",
        ]
 
        for part in source:
            total_position_value = float(part["price"]) * int(part["stock"])
            lines.append(
                f"- {safe_str(part['id'])} | {safe_str(part['name'])} | "
                f"Kategorie: {safe_str(part['category'])} | "
                f"Marke: {safe_str(part['brand'])} | "
                f"Preis: {format_currency(part['price'])} | "
                f"Bestand: {part['stock']} | "
                f"Gesamtwert: {format_currency(total_position_value)} | "
                f"Status: {safe_str(part['status'])}"
            )
 
        return "\n".join(lines)
 
    def filter_for_report(
        self,
        search_term: object = "",
        category_filter: object = "Alle",
        status_filter: object = "Alle",
    ) -> list[dict]:
        filtered = self.get_parts()
        term = safe_str(search_term).lower()
        category_filter = safe_str(category_filter)
        status_filter = safe_str(status_filter)
 
        if term:
            filtered = [
                part
                for part in filtered
                if term in safe_str(part.get("id")).lower()
                or term in safe_str(part.get("name")).lower()
                or term in safe_str(part.get("category")).lower()
                or term in safe_str(part.get("brand")).lower()
                or term in safe_str(part.get("status")).lower()
            ]
 
        if category_filter and category_filter != "Alle":
            filtered = [part for part in filtered if safe_str(part.get("category")) == category_filter]
 
        if status_filter and status_filter != "Alle":
            filtered = [part for part in filtered if safe_str(part.get("status")) == status_filter]
 
        return filtered