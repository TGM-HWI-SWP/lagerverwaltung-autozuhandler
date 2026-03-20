from __future__ import annotations

from copy import deepcopy

from src.ports.repositories import (
    CarRepositoryPort,
    CustomerRepositoryPort,
    PartRepositoryPort,
)


class InMemoryCarRepository(CarRepositoryPort):
    def __init__(self) -> None:
        self._cars: list[dict] = []

    def add(self, car: dict) -> None:
        self._cars.append(deepcopy(car))

    def get_all(self) -> list[dict]:
        return [deepcopy(car) for car in self._cars]

    def get_by_id(self, car_id: str) -> dict | None:
        for car in self._cars:
            if car.get("id") == car_id:
                return deepcopy(car)
        return None

    def update(self, car: dict) -> None:
        car_id = car.get("id")
        for index, current in enumerate(self._cars):
            if current.get("id") == car_id:
                self._cars[index] = deepcopy(car)
                return
        raise ValueError(f"Fahrzeug mit ID '{car_id}' wurde nicht gefunden.")

    def delete(self, car_id: str) -> bool:
        for index, car in enumerate(self._cars):
            if car.get("id") == car_id:
                del self._cars[index]
                return True
        return False

    def exists(self, car_id: str) -> bool:
        return any(car.get("id") == car_id for car in self._cars)


class InMemoryPartRepository(PartRepositoryPort):
    def __init__(self) -> None:
        self._parts: list[dict] = []

    def add(self, part: dict) -> None:
        self._parts.append(deepcopy(part))

    def get_all(self) -> list[dict]:
        return [deepcopy(part) for part in self._parts]

    def get_by_id(self, part_id: str) -> dict | None:
        for part in self._parts:
            if part.get("id") == part_id:
                return deepcopy(part)
        return None

    def update(self, part: dict) -> None:
        part_id = part.get("id")
        for index, current in enumerate(self._parts):
            if current.get("id") == part_id:
                self._parts[index] = deepcopy(part)
                return
        raise ValueError(f"Teil mit ID '{part_id}' wurde nicht gefunden.")

    def delete(self, part_id: str) -> bool:
        for index, part in enumerate(self._parts):
            if part.get("id") == part_id:
                del self._parts[index]
                return True
        return False

    def exists(self, part_id: str) -> bool:
        return any(part.get("id") == part_id for part in self._parts)


class InMemoryCustomerRepository(CustomerRepositoryPort):
    def __init__(self) -> None:
        self._customers: list[dict] = []

    def add(self, customer: dict) -> None:
        self._customers.append(deepcopy(customer))

    def get_all(self) -> list[dict]:
        return [deepcopy(customer) for customer in self._customers]

    def get_by_id(self, customer_id: str) -> dict | None:
        for customer in self._customers:
            if customer.get("id") == customer_id:
                return deepcopy(customer)
        return None

    def update(self, customer: dict) -> None:
        customer_id = customer.get("id")
        for index, current in enumerate(self._customers):
            if current.get("id") == customer_id:
                self._customers[index] = deepcopy(customer)
                return
        raise ValueError(f"Kunde mit ID '{customer_id}' wurde nicht gefunden.")

    def delete(self, customer_id: str) -> bool:
        for index, customer in enumerate(self._customers):
            if customer.get("id") == customer_id:
                del self._customers[index]
                return True
        return False

    def exists(self, customer_id: str) -> bool:
        return any(customer.get("id") == customer_id for customer in self._customers)