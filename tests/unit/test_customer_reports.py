from __future__ import annotations
 
from src.adapters.memory_repositories import InMemoryCustomerRepository

from src.reports.customer_reports import CustomerReportService
 
 
def test_customer_report_empty_dataframe() -> None:

    report = CustomerReportService(customer_repository=InMemoryCustomerRepository())

    df = report.generate_dataframe()
 
    assert df.empty is True

    assert "E-Mail" in df.columns
 
 
def test_customer_report_stats() -> None:

    repo = InMemoryCustomerRepository()

    repo.add({

        "id": "KUN-0001",

        "name": "Anna",

        "phone": "123",

        "email": "anna@example.com",

        "address": "Wien",

    })

    repo.add({

        "id": "KUN-0002",

        "name": "Paul",

        "phone": "",

        "email": "",

        "address": "Linz",

    })
 
    report = CustomerReportService(customer_repository=repo)

    total, with_email, with_phone = report.get_stats()
 
    assert total == "2"

    assert with_email == "1"

    assert with_phone == "1"
 
 
def test_customer_report_text_contains_values() -> None:

    repo = InMemoryCustomerRepository()

    repo.add({

        "id": "KUN-0001",

        "name": "Julia",

        "phone": "555",

        "email": "julia@example.com",

        "address": "Graz",

    })
 
    report = CustomerReportService(customer_repository=repo)

    text = report.generate_text_report()
 
    assert "Kundenreport" in text

    assert "Julia" in text

    assert "julia@example.com" in text
 