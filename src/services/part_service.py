from src.domain.models.part import Part
from src.services.formatting_service import smart_capitalize, safe_str


class PartService:
    def __init__(self, part_repo):
        self.part_repo = part_repo

    def add_part(self, part_id, name, category, brand, price, stock, status):
        part_id = safe_str(part_id).upper()
        name = smart_capitalize(name)
        category = smart_capitalize(category)
        brand = smart_capitalize(brand)

        if not all([part_id, name, category, brand, price, stock, status]):
            raise ValueError("Bitte alle Felder ausfüllen.")

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            raise ValueError("Preis muss eine Zahl sein, Bestand eine ganze Zahl.")

        if price < 0 or stock < 0:
            raise ValueError("Bitte gültige Werte eingeben.")

        if self.part_repo.get_by_id(part_id):
            raise ValueError(f"Die Teile-ID '{part_id}' existiert bereits.")

        part = Part(
            id=part_id,
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            status=status,
        )
        self.part_repo.add(part)
        return part

    def get_part(self, part_id: str):
        return self.part_repo.get_by_id(part_id)

    def update_part(self, selected_id, name, category, brand, price, stock, status):
        part = self.part_repo.get_by_id(selected_id)
        if not part:
            raise ValueError("Teil nicht gefunden.")

        name = smart_capitalize(name)
        category = smart_capitalize(category)
        brand = smart_capitalize(brand)

        if not all([name, category, brand, price, stock, status]):
            raise ValueError("Bitte alle Felder korrekt ausfüllen.")

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            raise ValueError("Preis muss eine Zahl sein, Bestand eine ganze Zahl.")

        part.name = name
        part.category = category
        part.brand = brand
        part.price = price
        part.stock = stock
        part.status = status

        self.part_repo.update(part)
        return part

    def delete_part(self, selected_id: str):
        part = self.part_repo.get_by_id(selected_id)
        if not part:
            raise ValueError("Teil nicht gefunden.")
        self.part_repo.delete(selected_id)
        return part

    def list_all(self):
        return self.part_repo.list_all()