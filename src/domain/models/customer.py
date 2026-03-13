from dataclasses import dataclass


@dataclass
class Part:
    id: str
    name: str
    category: str
    brand: str
    price: float
    stock: int
    status: str = "Verfügbar"