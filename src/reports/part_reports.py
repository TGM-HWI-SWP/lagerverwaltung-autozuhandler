from __future__ import annotations
 
from datetime import datetime
 
import pandas as pd
 
from src.ports.repositories import PartRepositoryPort

from src.services.formatting_service import format_currency, part_status_badge
 
 
class PartReportService:

    def __init__(self, part_repository: PartRepositoryPort) -> None:

        self.part_repository = part_repository
 
    def get_parts(self) -> list[dict]:

        return self.part_repository.get_all()
 
    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:

        source = data if data is not None else self.get_parts()
 
        if not source:

            return pd.DataFrame(

                columns=["ID", "Name", "Kategorie", "Marke", "Preis", "Bestand", "Gesamtwert", "Status"]

            )
 
        rows: list[dict] = []

        for part in source:

            total_value = float(part["price"]) * int(part["stock"])

            rows.append({

                "ID": part["id"],

                "Name": part["name"],

                "Kategorie": part["category"],

                "Marke": part["brand"],

                "Preis": format_currency(part["price"]),

                "Bestand": part["stock"],

                "Gesamtwert": format_currency(total_value),

                "Status": part_status_badge(part["status"]),

            })
 
        return pd.DataFrame(rows)
 
    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str, str]:

        source = data if data is not None else self.get_parts()
 
        total = len(source)

        stock = sum(int(part["stock"]) for part in source)

        total_value = sum(float(part["price"]) * int(part["stock"]) for part in source)
 
        if source:

            top = max(source, key=lambda x: float(x["price"]) * int(x["stock"]))

            top_text = f"{top['name']} ({format_currency(float(top['price']) * int(top['stock']))})"

        else:

            top_text = "-"
 
        return str(total), str(stock), format_currency(total_value), top_text
 
    def generate_text_report(self, data: list[dict] | None = None) -> str:

        source = data if data is not None else self.get_parts()
 
        if not source:

            return "Kein Teile-Report möglich, da noch keine Teile vorhanden sind."
 
        total, total_stock, total_value, top_text = self.get_stats(source)
 
        lines = [

            "Autozuhändler – Teile-Report",

            "=============================",

            f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",

            "",

            f"Teile gesamt: {total}",

            f"Gesamtstückzahl Lager: {total_stock}",

            f"Gesamtwert Teilelager: {total_value}",

            f"Wertvollstes Teil: {top_text}",

            "",

            "Teileliste:",

        ]
 
        for part in source:

            lines.append(

                f"- {part['id']} | {part['name']} | Kategorie: {part['category']} | "

                f"Marke: {part['brand']} | Preis: {format_currency(part['price'])} | "

                f"Bestand: {part['stock']} | Status: {part['status']}"

            )
 
        return "\n".join(lines)
 