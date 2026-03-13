from datetime import datetime
from src.domain.models.car import Car
from src.services.formatting_service import smart_capitalize, safe_str


class CarService:
    def __init__(self, car_repo, customer_repo):
        self.car_repo = car_repo
        self.customer_repo = customer_repo

    def add_car(
        self,
        car_id, brand, model, year, mileage, fuel, color,
        purchase_price, sale_price, customer_id, invoice_status, status
    ):
        car_id = safe_str(car_id).upper()
        brand = smart_capitalize(brand)
        model = smart_capitalize(model)
        color = smart_capitalize(color)

        if not all([car_id, brand, model, year, mileage, fuel, color, purchase_price, sale_price, invoice_status, status]):
            raise ValueError("Bitte alle Pflichtfelder ausfüllen.")

        try:
            year = int(year)
            mileage = int(mileage)
            purchase_price = float(purchase_price)
            sale_price = float(sale_price)
        except ValueError:
            raise ValueError("Baujahr und Kilometerstand müssen ganze Zahlen sein. Preise müssen Zahlen sein.")

        if year < 1900 or mileage < 0 or purchase_price < 0 or sale_price < 0:
            raise ValueError("Bitte gültige Werte eingeben.")

        if self.car_repo.get_by_id(car_id):
            raise ValueError(f"Die Fahrzeug-ID '{car_id}' existiert bereits.")

        sale_date = datetime.now().strftime("%d.%m.%Y") if status == "Verkauft" else ""

        car = Car(
            id=car_id,
            brand=brand,
            model=model,
            year=year,
            mileage=mileage,
            fuel=fuel,
            color=color,
            purchase_price=purchase_price,
            sale_price=sale_price,
            customer_id=customer_id,
            sale_date=sale_date,
            invoice_status=invoice_status,
            status=status,
        )
        self.car_repo.add(car)
        return car

    def get_car(self, car_id: str):
        return self.car_repo.get_by_id(car_id)

    def update_car(
        self,
        selected_id, brand, model, fuel, year, mileage, color,
        purchase_price, sale_price, customer_id, invoice_status, status
    ):
        car = self.car_repo.get_by_id(selected_id)
        if not car:
            raise ValueError("Fahrzeug nicht gefunden.")

        brand = smart_capitalize(brand)
        model = smart_capitalize(model)
        color = smart_capitalize(color)

        if not all([brand, model, fuel, year, mileage, color, purchase_price, sale_price, invoice_status, status]):
            raise ValueError("Bitte alle Pflichtfelder ausfüllen.")

        try:
            year = int(year)
            mileage = int(mileage)
            purchase_price = float(purchase_price)
            sale_price = float(sale_price)
        except ValueError:
            raise ValueError("Baujahr und Kilometerstand müssen ganze Zahlen sein. Preise müssen Zahlen sein.")

        car.brand = brand
        car.model = model
        car.fuel = fuel
        car.year = year
        car.mileage = mileage
        car.color = color
        car.purchase_price = purchase_price
        car.sale_price = sale_price
        car.customer_id = customer_id
        car.invoice_status = invoice_status
        car.status = status
        car.sale_date = datetime.now().strftime("%d.%m.%Y") if status == "Verkauft" else ""

        self.car_repo.update(car)
        return car

    def delete_car(self, selected_id: str):
        car = self.car_repo.get_by_id(selected_id)
        if not car:
            raise ValueError("Fahrzeug nicht gefunden.")
        self.car_repo.delete(selected_id)
        return car

    def list_all(self):
        return self.car_repo.list_all()