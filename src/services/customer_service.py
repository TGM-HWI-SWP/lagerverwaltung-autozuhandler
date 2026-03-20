from __future__ import annotations

from typing import Optional

from domain.models.customer import Customer
from ports.repositories import CarRepository, CustomerRepository
from services.formatting_service import safe_str, smart_capitalize
from services.id_service import get_next_customer_id


class CustomerService:
    def __init__(self, customer_repo: CustomerRepository, car_repo: CarRepository) -> None:
        self.customer_repo = customer_repo
        self.car_repo = car_repo

    def list_all(self) -> list[Customer]:
        return self.customer_repo.list_all()

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        return self.customer_repo.get_by_id(safe_str(customer_id))

    def get_next_id(self) -> str:
        return get_next_customer_id(self.customer_repo)

    def get_customer_choices(self, include_empty: bool = True) -> list[str]:
        choices: list[str] = []
        if include_empty:
            choices.append("-")

        for customer in self.customer_repo.list_all():
            choices.append(f"{customer.id} | {customer.name}")

        return choices

    def extract_customer_id(self, choice: str) -> str:
        value = safe_str(choice)
        if not value or value == "-":
            return ""
        return value.split("|")[0].strip()

    def get_customer_name_by_id(self, customer_id: str) -> str:
        customer = self.customer_repo.get_by_id(safe_str(customer_id))
        return customer.name if customer else "-"

    def create(
        self,
        customer_id: str,
        name: str,
        phone: str,
        email: str,
        address: str,
    ) -> Customer:
        normalized_id = safe_str(customer_id).upper() or self.get_next_id()

        if self.customer_repo.exists(normalized_id):
            raise ValueError(f"Die Kunden-ID '{normalized_id}' existiert bereits.")

        customer = self._build_customer(
            customer_id=normalized_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
        )
        self.customer_repo.add(customer)
        return customer

    def update(
        self,
        selected_id: str,
        name: str,
        phone: str,
        email: str,
        address: str,
    ) -> Customer:
        normalized_selected_id = safe_str(selected_id)
        if not normalized_selected_id:
            raise ValueError("Bitte zuerst einen Kunden zum Bearbeiten auswählen.")

        existing = self.customer_repo.get_by_id(normalized_selected_id)
        if existing is None:
            raise ValueError("Kunde nicht gefunden.")

        updated = self._build_customer(
            customer_id=existing.id,
            name=name,
            phone=phone,
            email=email,
            address=address,
        )
        self.customer_repo.update(updated)
        return updated

    def delete(self, selected_id: str) -> Customer:
        normalized_selected_id = safe_str(selected_id)
        if not normalized_selected_id:
            raise ValueError("Bitte zuerst einen Kunden auswählen.")

        existing = self.customer_repo.get_by_id(normalized_selected_id)
        if existing is None:
            raise ValueError("Kunde nicht gefunden.")

        used_by_car = next(
            (car for car in self.car_repo.list_all() if car.customer_id == normalized_selected_id),
            None,
        )
        if used_by_car is not None:
            raise ValueError(
                f"Kunde '{normalized_selected_id}' ist noch mit Fahrzeug '{used_by_car.id}' verknüpft und kann nicht gelöscht werden."
            )

        self.customer_repo.delete(normalized_selected_id)
        return existing

    def filter(self, search_term: str = "") -> list[Customer]:
        customers = self.customer_repo.list_all()
        term = safe_str(search_term).lower()

        if term:
            customers = [
                customer for customer in customers
                if term in customer.id.lower()
                or term in customer.name.lower()
                or term in customer.phone.lower()
                or term in customer.email.lower()
                or term in customer.address.lower()
            ]

        return customers

    def _build_customer(
        self,
        customer_id: str,
        name: str,
        phone: str,
        email: str,
        address: str,
    ) -> Customer:
        normalized_name = smart_capitalize(name)
        normalized_address = smart_capitalize(address)

        if not normalized_name:
            raise ValueError("Bitte mindestens den Kundennamen eingeben.")

        return Customer(
            id=customer_id,
            name=normalized_name,
            phone=safe_str(phone),
            email=safe_str(email),
            address=normalized_address,
        )