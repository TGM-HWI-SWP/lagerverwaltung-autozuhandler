from dataclasses import dataclass
from typing import Optional


@dataclass
class Car:
    id: str
    brand: str
    model: str
    year: int
    mileage: int
    fuel: str
    color: str
    purchase_price: float
    sale_price: float
    customer_id: Optional[str] = ""
    sale_date: str = ""
    invoice_status: str = "Offen"
    status: str = "Verfügbar"