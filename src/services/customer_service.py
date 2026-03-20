from __future__ import annotations

from src.ports.repositories import CarRepositoryPort, CustomerRepositoryPort
from src.services.formatting_service import safe_str, smart_capitalize
from src.services.id_service import get_next_customer_id
from src.services.service_result import ServiceResult 


class CustomerService:
    def __init__(
        self,
        customer_repository: CustomerRepositoryPort,
        car_repository: CarRepositoryPort,
    ) -> None:
        self.customer_repository = customer_repository
        self.car_repository = car_repository
 
    def get_all(self) -> list[dict]:
        return self.customer_repository.get_all()
 
    def get_by_id(self, customer_id: str) -> dict | None:
        return self.customer_repository.get_by_id(safe_str(customer_id).upper())
 
    def get_next_id(self) -> str:
        existing_ids = [customer["id"] for customer in self.customer_repository.get_all()]
        return get_next_customer_id(existing_ids)
 
    def create_customer(
        self,
        customer_id: str,
        name: object,
        phone: object,
        email: object,
        address: object,
    ) -> ServiceResult:
        prepared = self._validate_and_prepare(
            customer_id=customer_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
            editing_existing_id=None,
        )
 
        if not prepared.success:
            return prepared
 
        customer = prepared.data["customer"]
        self.customer_repository.add(customer)
 
        return ServiceResult.ok(
            f"Kunde '{customer['name']}' wurde gespeichert.",
            customer=customer,
        )
 
    def update_customer(
        self,
        selected_id: str,
        customer_id: str,
        name: object,
        phone: object,
        email: object,
        address: object,
    ) -> ServiceResult:
        selected_id = safe_str(selected_id).upper()
        if not selected_id:
            return ServiceResult.fail("Bitte zuerst einen Kunden zum Bearbeiten auswählen.")
 
        existing = self.customer_repository.get_by_id(selected_id)
        if not existing:
            return ServiceResult.fail("Kunde nicht gefunden.")
 
        prepared = self._validate_and_prepare(
            customer_id=customer_id or selected_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
            editing_existing_id=selected_id,
        )
 
        if not prepared.success:
            return prepared
 
        customer = prepared.data["customer"]
        customer["id"] = selected_id
        self.customer_repository.update(customer)
 
        return ServiceResult.ok(
            f"Kunde '{selected_id}' wurde aktualisiert.",
            customer=customer,
        )
 
    def delete_customer(self, selected_id: str) -> ServiceResult:
        selected_id = safe_str(selected_id).upper()
 
        if not selected_id:
            return ServiceResult.fail("Bitte zuerst einen Kunden auswählen.")
 
        existing = self.customer_repository.get_by_id(selected_id)
        if not existing:
            return ServiceResult.fail("Kunde nicht gefunden.")
 
        used_by_car = next(
            (car for car in self.car_repository.get_all() if safe_str(car.get("customer_id")).upper() == selected_id),
            None,
        )
        if used_by_car:
            return ServiceResult.fail(
                f"Kunde '{selected_id}' ist noch mit Fahrzeug '{used_by_car['id']}' verknüpft und kann nicht gelöscht werden."
            )
 
        deleted = self.customer_repository.delete(selected_id)
        if not deleted:
            return ServiceResult.fail("Kunde konnte nicht gelöscht werden.")
 
        return ServiceResult.ok(
            f"Kunde '{selected_id}' ({existing['name']}) wurde gelöscht."
        )
 
    def filter_customers(self, search_term: object = "") -> list[dict]:
        filtered = self.customer_repository.get_all()
        term = safe_str(search_term).lower()
 
        if term:
            filtered = [
                customer
                for customer in filtered
                if term in safe_str(customer.get("id")).lower()
                or term in safe_str(customer.get("name")).lower()
                or term in safe_str(customer.get("phone")).lower()
                or term in safe_str(customer.get("email")).lower()
                or term in safe_str(customer.get("address")).lower()
            ]
 
        return filtered
 
    def _validate_and_prepare(
        self,
        customer_id: object,
        name: object,
        phone: object,
        email: object,
        address: object,
        editing_existing_id: str | None,
    ) -> ServiceResult:
        prepared_id = safe_str(customer_id).upper() or self.get_next_id()
        prepared_name = smart_capitalize(name)
        prepared_phone = safe_str(phone)
        prepared_email = safe_str(email)
        prepared_address = smart_capitalize(address)
 
        if not prepared_name:
            return ServiceResult.fail("Bitte mindestens den Kundennamen eingeben.")
 
        if editing_existing_id is None and self.customer_repository.exists(prepared_id):
            return ServiceResult.fail(f"Die Kunden-ID '{prepared_id}' existiert bereits.")
 
        customer = {
            "id": prepared_id,
            "name": prepared_name,
            "phone": prepared_phone,
            "email": prepared_email,
            "address": prepared_address,
        }
 
        return ServiceResult.ok("Validierung erfolgreich.", customer=customer)