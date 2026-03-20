from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from domain.models.car import Car
from domain.models.part import Part
from domain.models.customer import Customer

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def list_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        raise NotImplementedError


class CarRepository(Repository[Car], ABC):
    pass


class PartRepository(Repository[Part], ABC):
    pass


class CustomerRepository(Repository[Customer], ABC):
    pass