from __future__ import annotations
 
from typing import Protocol
 
 
class CarRepositoryPort(Protocol):

    def add(self, car: dict) -> None:

        ...
 
    def get_all(self) -> list[dict]:

        ...
 
    def get_by_id(self, car_id: str) -> dict | None:

        ...
 
    def update(self, car: dict) -> None:

        ...
 
    def delete(self, car_id: str) -> bool:

        ...
 
    def exists(self, car_id: str) -> bool:

        ...
 
 
class PartRepositoryPort(Protocol):

    def add(self, part: dict) -> None:

        ...
 
    def get_all(self) -> list[dict]:

        ...
 
    def get_by_id(self, part_id: str) -> dict | None:

        ...
 
    def update(self, part: dict) -> None:

        ...
 
    def delete(self, part_id: str) -> bool:

        ...
 
    def exists(self, part_id: str) -> bool:

        ...
 
 
class CustomerRepositoryPort(Protocol):

    def add(self, customer: dict) -> None:

        ...
 
    def get_all(self) -> list[dict]:

        ...
 
    def get_by_id(self, customer_id: str) -> dict | None:

        ...
 
    def update(self, customer: dict) -> None:

        ...
 
    def delete(self, customer_id: str) -> bool:

        ...
 
    def exists(self, customer_id: str) -> bool:

        ...
 