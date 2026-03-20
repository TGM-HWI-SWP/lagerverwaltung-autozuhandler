from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Optional

from domain.enums import CarStatus, FuelType, InvoiceStatus
from domain.models.car import Car
from ports.repositories import CarRepository, CustomerRepository
from services.formatting_service import safe_str, smart_capitalize
from services.id_service import get_next_car_id


class CarService:
    def __init__(self, car_repo: CarRepository, customer_repo: CustomerRepository) -> None:
        self.car_repo = car_repo
        self.customer_repo = customer_repo

    def list_all(self) -> list[Car]:
        return self.car_repo.list_all()

    def get_by_id(self, car_id: str) -> Optional[Car]:
        return self.car_repo.get_by_id(safe_str(car_id))

    def get_next_id(self) -> str:
        return get_next_car_id(self.car_repo)

    def get_brand_choices(self) -> list[str]:
        brands = [car.brand for car in self.car_repo.list_all() if safe_str(car.brand)]
        seen: set[str] = set()
        result: list[str] = []

        for brand in sorted(brands, key=lambda x: x.lower()):
            if brand.lower() not in seen:
                seen.add(brand.lower())
                result.append(brand)

        return result

    def create(
        self,
        car_id: str,
        brand: str,
        model: str,
        year: str,
        mileage: str,
        fuel: str,
        color: str,
        purchase_price: str,
        sale_price: str,
        customer_id: str,
        invoice_status: str,
        status: str,
    ) -> Car:
        normalized_id = safe_str(car_id).upper() or self.get_next_id()

        if self.car_repo.exists(normalized_id):
            raise ValueError(f"Die Fahrzeug-ID '{normalized_id}' existiert bereits.")

        car = self._build_car(
            existing_car=None,
            car_id=normalized_id,
            brand=brand,
            model=model,
            year=year,
            mileage=mileage,
            fuel=fuel,
            color=color,
            purchase_price=purchase_price,
            sale_price=sale_price,
            customer_id=customer_id,
            invoice_status=invoice_status,
            status=status,
        )

        self.car_repo.add(car)
        return car

    def update(
        self,
        selected_id: str,
        brand: str,
        model: str,
        year: str,
        mileage: str,
        fuel: str,
        color: str,
        purchase_price: str,
        sale_price: str,
        customer_id: str,
        invoice_status: str,
        status: str,
    ) -> Car:
        normalized_selected_id = safe_str(selected_id)
        if not normalized_selected_id:
            raise ValueError("Bitte zuerst ein Fahrzeug zum Bearbeiten auswählen.")

        existing = self.car_repo.get_by_id(normalized_selected_id)
        if existing is None:
            raise ValueError("Fahrzeug nicht gefunden.")

        updated = self._build_car(
            existing_car=existing,
            car_id=existing.id,
            brand=brand,
            model=model,
            year=year,
            mileage=mileage,
            fuel=fuel,
            color=color,
            purchase_price=purchase_price,
            sale_price=sale_price,
            customer_id=customer_id,
            invoice_status=invoice_status,
            status=status,
        )

        self.car_repo.update(updated)
        return updated

    def delete(self, selected_id: str) -> Car:
        normalized_selected_id = safe_str(selected_id)
        if not normalized_selected_id:
            raise ValueError("Bitte zuerst ein Fahrzeug auswählen.")

        existing = self.car_repo.get_by_id(normalized_selected_id)
        if existing is None:
            raise ValueError("Fahrzeug nicht gefunden.")

        self.car_repo.delete(normalized_selected_id)
        return existing

    def filter(
        self,
        search_term: str = "",
        brand_filter: str = "Alle",
        status_filter: str = "Alle",
    ) -> list[Car]:
        cars = self.car_repo.list_all()
        term = safe_str(search_term).lower()

        if term:
            filtered: list[Car] = []
            for car in cars:
                customer_name = self._get_customer_name(car.customer_id).lower()
                haystack = [
                    car.id.lower(),
                    car.brand.lower(),
                    car.model.lower(),
                    car.fuel.value.lower(),
                    car.color.lower(),
                    car.status.value.lower(),
                    customer_name,
                ]
                if any(term in value for value in haystack):
                    filtered.append(car)
            cars = filtered

        if brand_filter != "Alle":
            cars = [car for car in cars if car.brand == brand_filter]

        if status_filter != "Alle":
            cars = [car for car in cars if car.status.value == status_filter]

        return cars

    def _build_car(
        self,
        existing_car: Optional[Car],
        car_id: str,
        brand: str,
        model: str,
        year: str,
        mileage: str,
        fuel: str,
        color: str,
        purchase_price: str,
        sale_price: str,
        customer_id: str,
        invoice_status: str,
        status: str,
    ) -> Car:
        normalized_brand = smart_capitalize(brand)
        normalized_model = smart_capitalize(model)
        normalized_color = smart_capitalize(color)
        normalized_customer_id = safe_str(customer_id)

        if not all([
            normalized_brand,
            normalized_model,
            safe_str(year),
            safe_str(mileage),
            safe_str(fuel),
            normalized_color,
            safe_str(purchase_price),
            safe_str(sale_price),
            safe_str(invoice_status),
            safe_str(status),
        ]):
            raise ValueError("Bitte alle Pflichtfelder ausfüllen.")

        try:
            parsed_year = int(year)
            parsed_mileage = int(mileage)
            parsed_purchase_price = float(purchase_price)
            parsed_sale_price = float(sale_price)
        except ValueError as exc:
            raise ValueError(
                "Baujahr und Kilometerstand müssen ganze Zahlen sein. Preise müssen Zahlen sein."
            ) from exc

        if parsed_year < 1900 or parsed_mileage < 0 or parsed_purchase_price < 0 or parsed_sale_price < 0:
            raise ValueError("Bitte gültige Werte eingeben.")

        if normalized_customer_id and self.customer_repo.get_by_id(normalized_customer_id) is None:
            raise ValueError(f"Kunde '{normalized_customer_id}' wurde nicht gefunden.")

        new_status = CarStatus(status)
        old_status = existing_car.status if existing_car else None

        sale_date = ""
        if new_status == CarStatus.SOLD:
            if existing_car and old_status == CarStatus.SOLD and existing_car.sale_date:
                sale_date = existing_car.sale_date
            else:
                sale_date = datetime.now().strftime("%d.%m.%Y")
        elif existing_car:
            sale_date = ""

        return Car(
            id=car_id,
            brand=normalized_brand,
            model=normalized_model,
            year=parsed_year,
            mileage=parsed_mileage,
            fuel=FuelType(fuel),
            color=normalized_color,
            purchase_price=parsed_purchase_price,
            sale_price=parsed_sale_price,
            customer_id=normalized_customer_id or None,
            sale_date=sale_date,
            invoice_status=InvoiceStatus(invoice_status),
            status=new_status,
        )

    def _get_customer_name(self, customer_id: str | None) -> str:
        if not customer_id:
            return ""
        customer = self.customer_repo.get_by_id(customer_id)
        return customer.name if customer else ""