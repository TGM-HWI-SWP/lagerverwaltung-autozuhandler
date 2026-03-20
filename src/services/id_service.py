from __future__ import annotations
 
 
def generate_next_id(prefix: str, existing_ids: list[str]) -> str:
    numbers: list[int] = []
 
    for item_id in existing_ids:
        if isinstance(item_id, str) and item_id.startswith(prefix + "-"):
            try:
                numbers.append(int(item_id.split("-")[1]))
            except Exception:
                pass
 
    next_number = max(numbers, default=0) + 1
    return f"{prefix}-{next_number:04d}"
 
 
def get_next_car_id(existing_ids: list[str]) -> str:
    return generate_next_id("CAR", existing_ids)
 
 
def get_next_part_id(existing_ids: list[str]) -> str:
    return generate_next_id("PRT", existing_ids)
 
 
def get_next_customer_id(existing_ids: list[str]) -> str:
    return generate_next_id("KUN", existing_ids)