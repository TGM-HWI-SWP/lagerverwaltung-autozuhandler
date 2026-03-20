from __future__ import annotations

from dataclasses import dataclass

from domain.enums import CarStatus, PartStatus
from domain.models.car import Car
from domain.models.customer import Customer
from domain.models.part import Part
from services.formatting_service import format_currency


@dataclass(frozen=True)
class CarDashboardStats:
    total: int
    available: int
    sold: int
    reserved: int
    total_profit: float
    top_sale_text: str


@dataclass(frozen=True)
class PartDashboardStats:
    total: int
    total_stock: int
    total_value: float
    top_value_text: str


@dataclass(frozen=True)
class CustomerDashboardStats:
    total: int
    with_email: int
    with_phone: int
    without_contact: int


class DashboardService:
    def get_car_stats(self, cars: list[Car]) -> CarDashboardStats:
        total = len(cars)
        available = sum(1 for car in cars if car.status == CarStatus.AVAILABLE)
        reserved = sum(1 for car in cars if car.status == CarStatus.RESERVED)
        sold = sum(1 for car in cars if car.status == CarStatus.SOLD)
        total_profit = sum(car.profit for car in cars)

        if cars:
            top = max(cars, key=lambda x: x.sale_price)
            top_sale_text = f"{top.brand} {top.model} ({top.sale_price:.2f} €)"
        else:
            top_sale_text = "-"

        return CarDashboardStats(
            total=total,
            available=available,
            sold=sold,
            reserved=reserved,
            total_profit=total_profit,
            top_sale_text=top_sale_text,
        )

    def get_part_stats(self, parts: list[Part]) -> PartDashboardStats:
        total = len(parts)
        total_stock = sum(part.stock for part in parts)
        total_value = sum(part.total_value for part in parts)

        if parts:
            top = max(parts, key=lambda x: x.total_value)
            top_value_text = f"{top.name} ({format_currency(top.total_value)})"
        else:
            top_value_text = "-"

        return PartDashboardStats(
            total=total,
            total_stock=total_stock,
            total_value=total_value,
            top_value_text=top_value_text,
        )

    def get_customer_stats(self, customers: list[Customer]) -> CustomerDashboardStats:
        total = len(customers)
        with_email = sum(1 for customer in customers if customer.email.strip())
        with_phone = sum(1 for customer in customers if customer.phone.strip())
        without_contact = sum(
            1 for customer in customers
            if not customer.email.strip() and not customer.phone.strip()
        )

        return CustomerDashboardStats(
            total=total,
            with_email=with_email,
            with_phone=with_phone,
            without_contact=without_contact,
        )