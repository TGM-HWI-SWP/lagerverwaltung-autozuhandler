from __future__ import annotations

from datetime import datetime

from domain.models.customer import Customer


def generate_customer_report(customers: list[Customer]) -> str:
    if not customers:
        return "Kein Kundenreport möglich, da noch keine Kunden vorhanden sind."

    lines = [
        "Autozuhändler – Kundenreport",
        "============================",
        f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
        "",
        f"Kunden gesamt: {len(customers)}",
        "",
        "Kundenliste:",
    ]

    for customer in customers:
        lines.append(
            f"- {customer.id} | {customer.name} | Telefon: {customer.phone} | "
            f"E-Mail: {customer.email} | Adresse: {customer.address}"
        )

    return "\n".join(lines)