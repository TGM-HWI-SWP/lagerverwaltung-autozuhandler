from __future__ import annotations

from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection

from src.ports.repositories import CarRepositoryPort


class MongoCarRepository(CarRepositoryPort):
    def __init__(
        self,
        mongo_uri: str,
        database_name: str = "autozuhaendler",
        collection_name: str = "cars",
    ) -> None:
        self._client = MongoClient(mongo_uri)
        self._db = self._client[database_name]
        self._collection: Collection = self._db[collection_name]

        self._collection.create_index("id", unique=True)

    def add(self, car: dict) -> None:
        document = self._to_document(car)
        self._collection.insert_one(document)

    def get_all(self) -> list[dict]:
        documents = list(self._collection.find({}, {"_id": 0}))
        return [self._from_document(doc) for doc in documents]

    def get_by_id(self, car_id: str) -> dict | None:
        document = self._collection.find_one({"id": car_id}, {"_id": 0})
        if not document:
            return None
        return self._from_document(document)

    def update(self, car: dict) -> None:
        result = self._collection.replace_one(
            {"id": car["id"]},
            self._to_document(car),
            upsert=False,
        )
        if result.matched_count == 0:
            raise ValueError(f"Fahrzeug mit ID '{car['id']}' wurde nicht gefunden.")

    def delete(self, car_id: str) -> bool:
        result = self._collection.delete_one({"id": car_id})
        return result.deleted_count > 0

    def exists(self, car_id: str) -> bool:
        return self._collection.count_documents({"id": car_id}, limit=1) > 0

    def _to_document(self, car: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": car.get("id", ""),
            "brand": car.get("brand", ""),
            "model": car.get("model", ""),
            "year": int(car.get("year", 0)),
            "mileage": int(car.get("mileage", 0)),
            "fuel": car.get("fuel", ""),
            "color": car.get("color", ""),
            "purchase_price": float(car.get("purchase_price", 0.0)),
            "sale_price": float(car.get("sale_price", 0.0)),
            "customer_id": car.get("customer_id", ""),
            "sale_date": car.get("sale_date", ""),
            "invoice_status": car.get("invoice_status", "Offen"),
            "status": car.get("status", "Verfügbar"),
        }

    def _from_document(self, document: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": document.get("id", ""),
            "brand": document.get("brand", ""),
            "model": document.get("model", ""),
            "year": int(document.get("year", 0)),
            "mileage": int(document.get("mileage", 0)),
            "fuel": document.get("fuel", ""),
            "color": document.get("color", ""),
            "purchase_price": float(document.get("purchase_price", 0.0)),
            "sale_price": float(document.get("sale_price", 0.0)),
            "customer_id": document.get("customer_id", ""),
            "sale_date": document.get("sale_date", ""),
            "invoice_status": document.get("invoice_status", "Offen"),
            "status": document.get("status", "Verfügbar"),
        }