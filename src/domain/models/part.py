from __future__ import annotations

from dataclasses import dataclass

from domain.enums import PartStatus


@dataclass
class Part:
    id: str
    name: str
    category: str
    brand: str
    price: float
    stock: int
    status: PartStatus = PartStatus.AVAILABLE

    @property
    def total_value(self) -> float:
        return self.price * self.stock