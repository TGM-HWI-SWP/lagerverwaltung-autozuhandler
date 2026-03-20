from __future__ import annotations

from src.services.formatting_service import safe_str


def normalize_db_list(values: list[object]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        prepared = safe_str(value)
        if prepared and prepared.lower() not in seen:
            seen.add(prepared.lower())
            result.append(prepared)

    result.sort(key=lambda x: x.lower())
    return result


def get_brand_choices(cars: list[dict]) -> list[str]:
    return normalize_db_list([car.get("brand", "") for car in cars])


def get_category_choices(parts: list[dict]) -> list[str]:
    return normalize_db_list([part.get("category", "") for part in parts])


def get_car_id_choices(cars: list[dict]) -> list[str]:
    return [safe_str(car.get("id")) for car in cars if safe_str(car.get("id"))]


def get_part_id_choices(parts: list[dict]) -> list[str]:
    return [safe_str(part.get("id")) for part in parts if safe_str(part.get("id"))]


def get_customer_id_choices(customers: list[dict]) -> list[str]:
    return [safe_str(customer.get("id")) for customer in customers if safe_str(customer.get("id"))]


def get_customer_choices(customers: list[dict], include_empty: bool = True) -> list[str]:
    choices: list[str] = []
    if include_empty:
        choices.append("-")

    for customer in customers:
        customer_id = safe_str(customer.get("id"))
        customer_name = safe_str(customer.get("name"))
        if customer_id:
            choices.append(f"{customer_id} | {customer_name}")

    return choices


def extract_customer_id(choice: object) -> str:
    prepared = safe_str(choice)
    if not prepared or prepared == "-":
        return ""
    return prepared.split("|")[0].strip()


def get_customer_choice_by_id(customers: list[dict], customer_id: object) -> str:
    prepared_id = safe_str(customer_id).upper()
    if not prepared_id:
        return "-"

    for customer in customers:
        if safe_str(customer.get("id")).upper() == prepared_id:
            return f"{prepared_id} | {safe_str(customer.get('name'))}"

    return "-"


def make_choice_suggestions(search_text: object, source_list: list[str], limit: int = 8) -> list[str]:
    prepared = safe_str(search_text).lower()
    if not prepared:
        return source_list[:limit]

    starts = [item for item in source_list if item.lower().startswith(prepared)]
    contains = [item for item in source_list if prepared in item.lower() and item not in starts]
    return (starts + contains)[:limit]