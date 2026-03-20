from __future__ import annotations

from datetime import datetime

from domain.models.part import Part
from services.formatting_service import format_currency


def generate_part_report(parts: list[Part]) -> str:
    if not parts:
        return "Kein Teile-Report möglich, da noch keine Teile vorhanden sind."

    total = len(parts)
    total_stock = sum(int(part.stock) for part in parts)
    total_value = sum(float(part.price) * int(part.stock) for part in parts)

    lines = [
        "Autozuhändler – Teile-Report",
        "=============================",
        f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
        "",
        f"Teile gesamt: {total}",
        f"Gesamtstückzahl Lager: {total_stock}",
        f"Gesamtwert Teilelager: {format_currency(total_value)}",
        "",
        "Teileliste:",
    ]

    for part in parts:
        lines.append(
            f"- {part.id} | {part.name} | Kategorie: {part.category} | "
            f"Marke: {part.brand} | Preis: {format_currency(part.price)} | "
            f"Bestand: {part.stock} | Status: {part.status.value}"
        )

    return "\n".join(lines)