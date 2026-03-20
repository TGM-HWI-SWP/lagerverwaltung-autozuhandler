from __future__ import annotations

from typing import Optional

from domain.enums import PartStatus
from domain.models.part import Part
from ports.repositories import PartRepository
from services.formatting_service import safe_str, smart_capitalize
from services.id_service import get_next_part_id


class PartService:
    def __init__(self, part_repo: PartRepository) -> None:
        self.part_repo = part_repo

    def list_all(self) -> list[Part]:
        return self.part_repo.list_all()

    def get_by_id(self, part_id: str) -> Optional[Part]:
        return self.part_repo.get_by_id(safe_str(part_id))

    def get_next_id(self) -> str:
        return get_next_part_id(self.part_repo)

    def get_category_choices(self) -> list[str]:
        categories = [part.category for part in self.part_repo.list_all() if safe_str(part.category)]
        seen: set[str] = set()
        result: list[str] = []

        for category in sorted(categories, key=lambda x: x.lower()):
            if category.lower() not in seen:
                seen.add(category.lower())
                result.append(category)

        return result

    def create(
        self,
        part_id: str,
        name: str,
        category: str,
        brand: str,
        price: str,
        stock: str,
        status: str,
    ) -> Part:
        normalized_id = safe_str(part_id).upper() or self.get_next_id()

        if self.part_repo.exists(normalized_id):
            raise ValueError(f"Die Teile-ID '{normalized_id}' existiert bereits.")

        part = self._build_part(
            part_id=normalized_id,
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            status=status,
        )
        self.part_repo.add(part)
        return part

    def update(
        self,
        selected_id: str,
        name: str,
        category: str,
        brand: str,
        price: str,
        stock: str,
        status: str,
    ) -> Part:
        normalized_selected_id = safe_str(selected_id)
        if not normalized_selected_id:
            raise ValueError("Bitte zuerst ein Teil zum Bearbeiten auswählen.")

        existing = self.part_repo.get_by_id(normalized_selected_id)
        if existing is None:
            raise ValueError("Teil nicht gefunden.")

        updated = self._build_part(
            part_id=existing.id,
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            status=status,
        )
        self.part_repo.update(updated)
        return updated

    def delete(self, selected_id: str) -> Part:
        normalized_selected_id = safe_str(selected_id)
        if not normalized_selected_id:
            raise ValueError("Bitte zuerst ein Teil auswählen.")

        existing = self.part_repo.get_by_id(normalized_selected_id)
        if existing is None:
            raise ValueError("Teil nicht gefunden.")

        self.part_repo.delete(normalized_selected_id)
        return existing

    def filter(
        self,
        search_term: str = "",
        category_filter: str = "Alle",
        status_filter: str = "Alle",
    ) -> list[Part]:
        parts = self.part_repo.list_all()
        term = safe_str(search_term).lower()

        if term:
            parts = [
                part for part in parts
                if term in part.id.lower()
                or term in part.name.lower()
                or term in part.category.lower()
                or term in part.brand.lower()
                or term in part.status.value.lower()
            ]

        if category_filter != "Alle":
            parts = [part for part in parts if part.category == category_filter]

        if status_filter != "Alle":
            parts = [part for part in parts if part.status.value == status_filter]

        return parts

    def _build_part(
        self,
        part_id: str,
        name: str,
        category: str,
        brand: str,
        price: str,
        stock: str,
        status: str,
    ) -> Part:
        normalized_name = smart_capitalize(name)
        normalized_category = smart_capitalize(category)
        normalized_brand = smart_capitalize(brand)

        if not all([
            normalized_name,
            normalized_category,
            normalized_brand,
            safe_str(price),
            safe_str(stock),
            safe_str(status),
        ]):
            raise ValueError("Bitte alle Felder ausfüllen.")

        try:
            parsed_price = float(price)
            parsed_stock = int(stock)
        except ValueError as exc:
            raise ValueError("Preis muss eine Zahl sein, Bestand eine ganze Zahl.") from exc

        if parsed_price < 0 or parsed_stock < 0:
            raise ValueError("Bitte gültige Werte eingeben.")

        return Part(
            id=part_id,
            name=normalized_name,
            category=normalized_category,
            brand=normalized_brand,
            price=parsed_price,
            stock=parsed_stock,
            status=PartStatus(status),
        )