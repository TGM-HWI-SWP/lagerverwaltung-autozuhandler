from __future__ import annotations

from typing import Dict, Optional

from domain.models.car import Car
from domain.models.customer import Customer
from domain.models.part import Part
from ports.repositories import CarRepository, CustomerRepository, PartRepository


class InMemoryCarRepository(CarRepository):
    def __init__(self) -> None:
        self._items: Dict[str, Car] = {}

    def list_all(self) -> list[Car]:
        return list(self._items.values())

    def get_by_id(self, entity_id: str) -> Optional[Car]:
        return self._items.get(entity_id)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._items

    def add(self, entity: Car) -> None:
        self._items[entity.id] = entity

    def update(self, entity: Car) -> None:
        self._items[entity.id] = entity

    def delete(self, entity_id: str) -> None:
        self._items.pop(entity_id, None)


class InMemoryPartRepository(PartRepository):
    def __init__(self) -> None:
        self._items: Dict[str, Part] = {}

    def list_all(self) -> list[Part]:
        return list(self._items.values())

    def get_by_id(self, entity_id: str) -> Optional[Part]:
        return self._items.get(entity_id)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._items

    def add(self, entity: Part) -> None:
        self._items[entity.id] = entity

    def update(self, entity: Part) -> None:
        self._items[entity.id] = entity

    def delete(self, entity_id: str) -> None:
        self._items.pop(entity_id, None)


class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self) -> None:
        self._items: Dict[str, Customer] = {}

    def list_all(self) -> list[Customer]:
        return list(self._items.values())

    def get_by_id(self, entity_id: str) -> Optional[Customer]:
        return self._items.get(entity_id)

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._items

    def add(self, entity: Customer) -> None:
        self._items[entity.id] = entity

    def update(self, entity: Customer) -> None:
        self._items[entity.id] = entity

    def delete(self, entity_id: str) -> None:
        self._items.pop(entity_id, None)