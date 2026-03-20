from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from domain.enums import CarStatus, FuelType, InvoiceStatus


@dataclass
class Car:
    id: str
    brand: str
    model: str
    year: int
    mileage: int
    fuel: FuelType
    color: str
    purchase_price: float
    sale_price: float
    customer_id: Optional[str] = None
    sale_date: str = ""
    invoice_status: InvoiceStatus = InvoiceStatus.OPEN
    status: CarStatus = CarStatus.AVAILABLE

    @property
    def profit(self) -> float:
        return self.sale_price - self.purchase_price