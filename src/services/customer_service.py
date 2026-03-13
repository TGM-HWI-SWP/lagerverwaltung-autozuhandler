from src.domain.models.customer import Customer
from src.services.formatting_service import smart_capitalize, safe_str


class CustomerService:
    def __init__(self, customer_repo, car_repo):
        self.customer_repo = customer_repo
        self.car_repo = car_repo

    def add_customer(self, customer_id, name, phone, email, address):
        customer_id = safe_str(customer_id).upper()
        name = smart_capitalize(name)
        address = smart_capitalize(address)

        if not name:
            raise ValueError("Bitte mindestens den Kundennamen eingeben.")

        if self.customer_repo.get_by_id(customer_id):
            raise ValueError(f"Die Kunden-ID '{customer_id}' existiert bereits.")

        customer = Customer(
            id=customer_id,
            name=name,
            phone=safe_str(phone),
            email=safe_str(email),
            address=address,
        )
        self.customer_repo.add(customer)
        return customer

    def get_customer(self, customer_id: str):
        return self.customer_repo.get_by_id(customer_id)

    def update_customer(self, selected_id, name, phone, email, address):
        customer = self.customer_repo.get_by_id(selected_id)
        if not customer:
            raise ValueError("Kunde nicht gefunden.")

        name = smart_capitalize(name)
        address = smart_capitalize(address)

        if not name:
            raise ValueError("Bitte mindestens den Kundennamen eingeben.")

        customer.name = name
        customer.phone = safe_str(phone)
        customer.email = safe_str(email)
        customer.address = address

        self.customer_repo.update(customer)
        return customer

    def delete_customer(self, selected_id: str):
        customer = self.customer_repo.get_by_id(selected_id)
        if not customer:
            raise ValueError("Kunde nicht gefunden.")

        used_by_car = next((car for car in self.car_repo.list_all() if car.customer_id == selected_id), None)
        if used_by_car:
            raise ValueError(
                f"Kunde '{selected_id}' ist noch mit Fahrzeug '{used_by_car.id}' verknüpft und kann nicht gelöscht werden."
            )

        self.customer_repo.delete(selected_id)
        return customer

    def list_all(self):
        return self.customer_repo.list_all()