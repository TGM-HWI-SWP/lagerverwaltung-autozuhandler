from __future__ import annotations
 
from src.ports.repositories import PartRepositoryPort
from src.services.formatting_service import safe_str, smart_capitalize
from src.services.id_service import get_next_part_id
from src.services.service_result import ServiceResult
 
 
PART_STATUSES = ["Verfügbar", "Nachbestellen", "Nicht verfügbar"]
 
 
class PartService:
    def __init__(self, part_repository: PartRepositoryPort) -> None:
        self.part_repository = part_repository
 
    def get_all(self) -> list[dict]:
        return self.part_repository.get_all()
 
    def get_by_id(self, part_id: str) -> dict | None:
        return self.part_repository.get_by_id(safe_str(part_id).upper())
 
    def get_next_id(self) -> str:
        existing_ids = [part["id"] for part in self.part_repository.get_all()]
        return get_next_part_id(existing_ids)
 
    def create_part(
        self,
        part_id: str,
        name: object,
        category: object,
        brand: object,
        price: object,
        stock: object,
        status: object,
    ) -> ServiceResult:
        prepared = self._validate_and_prepare(
            part_id=part_id,
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            status=status,
            editing_existing_id=None,
        )
 
        if not prepared.success:
            return prepared
 
        part = prepared.data["part"]
        self.part_repository.add(part)
 
        return ServiceResult.ok(
            f"Teil '{part['name']}' wurde gespeichert.",
            part=part,
        )
 
    def update_part(
        self,
        selected_id: str,
        part_id: str,
        name: object,
        category: object,
        brand: object,
        price: object,
        stock: object,
        status: object,
    ) -> ServiceResult:
        selected_id = safe_str(selected_id).upper()
        if not selected_id:
            return ServiceResult.fail("Bitte zuerst ein Teil zum Bearbeiten auswählen.")
 
        existing = self.part_repository.get_by_id(selected_id)
        if not existing:
            return ServiceResult.fail("Teil nicht gefunden.")
 
        prepared = self._validate_and_prepare(
            part_id=part_id or selected_id,
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            status=status,
            editing_existing_id=selected_id,
        )
 
        if not prepared.success:
            return prepared
 
        part = prepared.data["part"]
        part["id"] = selected_id
        self.part_repository.update(part)
 
        return ServiceResult.ok(
            f"Teil '{selected_id}' wurde aktualisiert.",
            part=part,
        )
 
    def delete_part(self, selected_id: str) -> ServiceResult:
        selected_id = safe_str(selected_id).upper()
 
        if not selected_id:
            return ServiceResult.fail("Bitte zuerst ein Teil auswählen.")
 
        existing = self.part_repository.get_by_id(selected_id)
        if not existing:
            return ServiceResult.fail("Teil nicht gefunden.")
 
        deleted_text = safe_str(existing.get("name"))
        deleted = self.part_repository.delete(selected_id)
 
        if not deleted:
            return ServiceResult.fail("Teil konnte nicht gelöscht werden.")
 
        return ServiceResult.ok(
            f"Teil '{selected_id}' ({deleted_text}) wurde gelöscht."
        )
 
    def filter_parts(
        self,
        search_term: object = "",
        category_filter: object = "Alle",
        status_filter: object = "Alle",
    ) -> list[dict]:
        filtered = self.part_repository.get_all()
 
        term = safe_str(search_term).lower()
        category_filter = safe_str(category_filter)
        status_filter = safe_str(status_filter)
 
        if term:
            filtered = [
                part
                for part in filtered
                if term in safe_str(part.get("id")).lower()
                or term in safe_str(part.get("name")).lower()
                or term in safe_str(part.get("category")).lower()
                or term in safe_str(part.get("brand")).lower()
                or term in safe_str(part.get("status")).lower()
            ]
 
        if category_filter and category_filter != "Alle":
            filtered = [part for part in filtered if safe_str(part.get("category")) == category_filter]
 
        if status_filter and status_filter != "Alle":
            filtered = [part for part in filtered if safe_str(part.get("status")) == status_filter]
 
        return filtered
 
    def _validate_and_prepare(
        self,
        part_id: object,
        name: object,
        category: object,
        brand: object,
        price: object,
        stock: object,
        status: object,
        editing_existing_id: str | None,
    ) -> ServiceResult:
        prepared_id = safe_str(part_id).upper() or self.get_next_id()
        prepared_name = smart_capitalize(name)
        prepared_category = smart_capitalize(category)
        prepared_brand = smart_capitalize(brand)
        prepared_status = safe_str(status)
 
        if not all([
            prepared_name,
            prepared_category,
            prepared_brand,
            safe_str(price),
            safe_str(stock),
            prepared_status,
        ]):
            return ServiceResult.fail("Bitte alle Felder ausfüllen.")
 
        if prepared_status not in PART_STATUSES:
            return ServiceResult.fail("Ungültiger Lagerstatus.")
 
        try:
            prepared_price = float(price)
            prepared_stock = int(stock)
        except ValueError:
            return ServiceResult.fail("Preis muss eine Zahl sein, Bestand eine ganze Zahl.")
 
        if prepared_price < 0 or prepared_stock < 0:
            return ServiceResult.fail("Bitte gültige Werte eingeben.")
 
        if editing_existing_id is None and self.part_repository.exists(prepared_id):
            return ServiceResult.fail(f"Die Teile-ID '{prepared_id}' existiert bereits.")
 
        part = {
            "id": prepared_id,
            "name": prepared_name,
            "category": prepared_category,
            "brand": prepared_brand,
            "price": prepared_price,
            "stock": prepared_stock,
            "status": prepared_status,
        }
 
        return ServiceResult.ok("Validierung erfolgreich.", part=part)