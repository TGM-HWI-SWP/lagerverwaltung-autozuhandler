from __future__ import annotations

from ports.repositories import CarRepository, CustomerRepository, PartRepository


def generate_next_id(prefix: str, existing_ids: list[str]) -> str:
    numbers: list[int] = []

    for item_id in existing_ids:
        if isinstance(item_id, str) and item_id.startswith(f"{prefix}-"):
            try:
                numbers.append(int(item_id.split("-")[1]))
            except (IndexError, ValueError):
                continue

    next_number = max(numbers, default=0) + 1
    return f"{prefix}-{next_number:04d}"


def get_next_car_id(car_repo: CarRepository) -> str:
    return generate_next_id("CAR", [car.id for car in car_repo.list_all()])


def get_next_part_id(part_repo: PartRepository) -> str:
    return generate_next_id("PRT", [part.id for part in part_repo.list_all()])


def get_next_customer_id(customer_repo: CustomerRepository) -> str:
    return generate_next_id("KUN", [customer.id for customer in customer_repo.list_all()])