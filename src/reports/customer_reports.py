from __future__ import annotations
 
from datetime import datetime
 
import pandas as pd
 
from src.ports.repositories import CustomerRepositoryPort

from src.services.formatting_service import safe_str
 
 
class CustomerReportService:

    def __init__(self, customer_repository: CustomerRepositoryPort) -> None:

        self.customer_repository = customer_repository
 
    def get_customers(self) -> list[dict]:

        return self.customer_repository.get_all()
 
    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:

        source = data if data is not None else self.get_customers()
 
        if not source:

            return pd.DataFrame(columns=["ID", "Name", "Telefon", "E-Mail", "Adresse"])
 
        rows: list[dict] = []

        for customer in source:

            rows.append({

                "ID": customer["id"],

                "Name": customer["name"],

                "Telefon": customer["phone"],

                "E-Mail": customer["email"],

                "Adresse": customer["address"],

            })
 
        return pd.DataFrame(rows)
 
    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str]:

        source = data if data is not None else self.get_customers()
 
        total = len(source)

        with_email = sum(1 for customer in source if safe_str(customer["email"]))

        with_phone = sum(1 for customer in source if safe_str(customer["phone"]))
 
        return str(total), str(with_email), str(with_phone)
 
    def generate_text_report(self, data: list[dict] | None = None) -> str:

        source = data if data is not None else self.get_customers()
 
        if not source:

            return "Kein Kundenreport möglich, da noch keine Kunden vorhanden sind."
 
        total, with_email, with_phone = self.get_stats(source)
 
        lines = [

            "Autozuhändler – Kundenreport",

            "============================",

            f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",

            "",

            f"Kunden gesamt: {total}",

            f"Mit E-Mail: {with_email}",

            f"Mit Telefon: {with_phone}",

            "",

            "Kundenliste:",

        ]
 
        for customer in source:

            lines.append(

                f"- {customer['id']} | {customer['name']} | Telefon: {customer['phone']} | "

                f"E-Mail: {customer['email']} | Adresse: {customer['address']}"

            )
 
        return "\n".join(lines)
 