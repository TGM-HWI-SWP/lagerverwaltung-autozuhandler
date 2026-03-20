from __future__ import annotations
 
from datetime import datetime
 
from src.ports.repositories import CarRepositoryPort, CustomerRepositoryPort
from src.services.formatting_service import safe_str, smart_capitalize
from src.services.id_service import get_next_car_id
from src.services.service_result import ServiceResult
 
 
CAR_STATUSES = ["Verfügbar", "Reserviert", "Verkauft"]
INVOICE_STATUSES = ["Offen", "Bezahlt", "Storniert"]
FUELS = ["Benzin", "Diesel", "Hybrid", "Elektro"]
 
 
class CarService:
    def __init__(
        self,
        car_repository: CarRepositoryPort,
        customer_repository: CustomerRepositoryPort,
    ) -> None:
        self.car_repository = car_repository
        self.customer_repository = customer_repository
 
    def get_all(self) -> list[dict]:
        return self.car_repository.get_all()
 
    def get_by_id(self, car_id: str) -> dict | None:
        return self.car_repository.get_by_id(safe_str(car_id).upper())
 
    def get_next_id(self) -> str:
        existing_ids = [car["id"] for car in self.car_repository.get_all()]
        return get_next_car_id(existing_ids)
 
    def create_car(
        self,
        car_id: str,
        brand: object,
        model: object,
        year: object,
        mileage: object,
        fuel: object,
        color: object,
        purchase_price: object,
        sale_price: object,
        customer_id: object = "",
        invoice_status: object = "Offen",
        status: object = "Verfügbar",
    ) -> ServiceResult:
        prepared = self._validate_and_prepare(
            car_id=car_id,
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
            editing_existing_id=None,
        )
 
        if not prepared.success:
            return prepared
 
        car = prepared.data["car"]
        self.car_repository.add(car)
 
        return ServiceResult.ok(
            f"Fahrzeug '{car['brand']} {car['model']}' wurde gespeichert.",
            car=car,
        )
 
    def update_car(
        self,
        selected_id: str,
        car_id: str,
        brand: object,
        model: object,
        year: object,
        mileage: object,
        fuel: object,
        color: object,
        purchase_price: object,
        sale_price: object,
        customer_id: object = "",
        invoice_status: object = "Offen",
        status: object = "Verfügbar",
    ) -> ServiceResult:
        selected_id = safe_str(selected_id).upper()
        if not selected_id:
            return ServiceResult.fail("Bitte zuerst ein Fahrzeug zum Bearbeiten auswählen.")
 
        existing = self.car_repository.get_by_id(selected_id)
        if not existing:
            return ServiceResult.fail("Fahrzeug nicht gefunden.")
 
        prepared = self._validate_and_prepare(
            car_id=car_id or selected_id,
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
            editing_existing_id=selected_id,
        )
 
        if not prepared.success:
            return prepared
 
        car = prepared.data["car"]
        car["id"] = selected_id
        self.car_repository.update(car)
 
        return ServiceResult.ok(
            f"Fahrzeug '{selected_id}' wurde aktualisiert.",
            car=car,
        )
 
    def delete_car(self, selected_id: str) -> ServiceResult:
        selected_id = safe_str(selected_id).upper()
 
        if not selected_id:
            return ServiceResult.fail("Bitte zuerst ein Fahrzeug auswählen.")
 
        existing = self.car_repository.get_by_id(selected_id)
        if not existing:
            return ServiceResult.fail("Fahrzeug nicht gefunden.")
 
        deleted_text = f"{existing['brand']} {existing['model']}"
        deleted = self.car_repository.delete(selected_id)
 
        if not deleted:
            return ServiceResult.fail("Fahrzeug konnte nicht gelöscht werden.")
 
        return ServiceResult.ok(
            f"Fahrzeug '{selected_id}' ({deleted_text}) wurde gelöscht."
        )
 
    def filter_cars(
        self,
        search_term: object = "",
        brand_filter: object = "Alle",
        status_filter: object = "Alle",
    ) -> list[dict]:
        filtered = self.car_repository.get_all()
 
        term = safe_str(search_term).lower()
        brand_filter = safe_str(brand_filter)
        status_filter = safe_str(status_filter)
 
        if term:
            filtered = [
                car
                for car in filtered
                if term in safe_str(car.get("id")).lower()
                or term in safe_str(car.get("brand")).lower()
                or term in safe_str(car.get("model")).lower()
                or term in safe_str(car.get("fuel")).lower()
                or term in safe_str(car.get("color")).lower()
                or term in safe_str(car.get("status")).lower()
                or term in self.get_customer_name_by_id(car.get("customer_id", "")).lower()
            ]
 
        if brand_filter and brand_filter != "Alle":
            filtered = [car for car in filtered if safe_str(car.get("brand")) == brand_filter]
 
        if status_filter and status_filter != "Alle":
            filtered = [car for car in filtered if safe_str(car.get("status")) == status_filter]
 
        return filtered
 
    def get_customer_name_by_id(self, customer_id: object) -> str:
        customer_id = safe_str(customer_id).upper()
        if not customer_id:
            return "-"
 
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            return "-"
        return safe_str(customer.get("name")) or "-"
 
    def _validate_and_prepare(
        self,
        car_id: object,
        brand: object,
        model: object,
        year: object,
        mileage: object,
        fuel: object,
        color: object,
        purchase_price: object,
        sale_price: object,
        customer_id: object,
        invoice_status: object,
        status: object,
        editing_existing_id: str | None,
    ) -> ServiceResult:
        prepared_id = safe_str(car_id).upper() or self.get_next_id()
        prepared_brand = smart_capitalize(brand)
        prepared_model = smart_capitalize(model)
        prepared_fuel = safe_str(fuel)
        prepared_color = smart_capitalize(color)
        prepared_customer_id = safe_str(customer_id).upper()
        prepared_invoice_status = safe_str(invoice_status)
        prepared_status = safe_str(status)
 
        if not all([
            prepared_brand,
            prepared_model,
            safe_str(year),
            safe_str(mileage),
            prepared_fuel,
            prepared_color,
            safe_str(purchase_price),
            safe_str(sale_price),
            prepared_invoice_status,
            prepared_status,
        ]):
            return ServiceResult.fail("Bitte alle Pflichtfelder ausfüllen.")
 
        if prepared_fuel not in FUELS:
            return ServiceResult.fail("Ungültiger Kraftstoff.")
 
        if prepared_invoice_status not in INVOICE_STATUSES:
            return ServiceResult.fail("Ungültiger Rechnungsstatus.")
 
        if prepared_status not in CAR_STATUSES:
            return ServiceResult.fail("Ungültiger Fahrzeugstatus.")
 
        try:
            prepared_year = int(year)
            prepared_mileage = int(mileage)
            prepared_purchase_price = float(purchase_price)
            prepared_sale_price = float(sale_price)
        except ValueError:
            return ServiceResult.fail(
                "Baujahr und Kilometerstand müssen ganze Zahlen sein. Preise müssen Zahlen sein."
            )
 
        if prepared_year < 1900:
            return ServiceResult.fail("Baujahr muss mindestens 1900 sein.")
 
        if prepared_mileage < 0:
            return ServiceResult.fail("Kilometerstand darf nicht negativ sein.")
 
        if prepared_purchase_price < 0 or prepared_sale_price < 0:
            return ServiceResult.fail("Preise dürfen nicht negativ sein.")
 
        if editing_existing_id is None and self.car_repository.exists(prepared_id):
            return ServiceResult.fail(f"Die Fahrzeug-ID '{prepared_id}' existiert bereits.")
 
        if prepared_customer_id and not self.customer_repository.exists(prepared_customer_id):
            return ServiceResult.fail(f"Der Kunde '{prepared_customer_id}' existiert nicht.")
 
        sale_date = datetime.now().strftime("%d.%m.%Y") if prepared_status == "Verkauft" else ""
 
        car = {
            "id": prepared_id,
            "brand": prepared_brand,
            "model": prepared_model,
            "year": prepared_year,
            "mileage": prepared_mileage,
            "fuel": prepared_fuel,
            "color": prepared_color,
            "purchase_price": prepared_purchase_price,
            "sale_price": prepared_sale_price,
            "customer_id": prepared_customer_id,
            "sale_date": sale_date,
            "invoice_status": prepared_invoice_status,
            "status": prepared_status,
        }
 
        return ServiceResult.ok("Validierung erfolgreich.", car=car)