def generate_next_id(prefix: str, existing_ids: list[str]) -> str:
    numbers = []
    for item_id in existing_ids:
        if isinstance(item_id, str) and item_id.startswith(prefix + "-"):
            try:
                numbers.append(int(item_id.split("-")[1]))
            except Exception:
                pass
    next_number = max(numbers, default=0) + 1
    return f"{prefix}-{next_number:04d}"


def get_next_car_id(car_repo) -> str:
    return generate_next_id("CAR", [car.id for car in car_repo.list_all()])


def get_next_part_id(part_repo) -> str:
    return generate_next_id("PRT", [part.id for part in part_repo.list_all()])


def get_next_customer_id(customer_repo) -> str:
    return generate_next_id("KUN", [customer.id for customer in customer_repo.list_all()])