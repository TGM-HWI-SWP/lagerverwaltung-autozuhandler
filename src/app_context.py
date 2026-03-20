from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from adapters.memory_repositories import (
    InMemoryCarRepository,
    InMemoryCustomerRepository,
    InMemoryPartRepository,
)
from ports.repositories import CarRepository, CustomerRepository, PartRepository
from services.auth_service import AuthService
from services.car_service import CarService
from services.customer_service import CustomerService
from services.dashboard_service import DashboardService
from services.part_service import PartService


@dataclass
class AppContext:
    car_repo: CarRepository
    part_repo: PartRepository
    customer_repo: CustomerRepository
    export_dir: Path

    auth_service: AuthService
    car_service: CarService
    part_service: PartService
    customer_service: CustomerService
    dashboard_service: DashboardService


def build_app_context() -> AppContext:
    export_dir = Path(r"C:\Nextcloud_Autozu\exports")
    export_dir.mkdir(parents=True, exist_ok=True)

    car_repo = InMemoryCarRepository()
    part_repo = InMemoryPartRepository()
    customer_repo = InMemoryCustomerRepository()

    auth_service = AuthService()
    car_service = CarService(car_repo=car_repo, customer_repo=customer_repo)
    part_service = PartService(part_repo=part_repo)
    customer_service = CustomerService(customer_repo=customer_repo, car_repo=car_repo)
    dashboard_service = DashboardService()

    return AppContext(
        car_repo=car_repo,
        part_repo=part_repo,
        customer_repo=customer_repo,
        export_dir=export_dir,
        auth_service=auth_service,
        car_service=car_service,
        part_service=part_service,
        customer_service=customer_service,
        dashboard_service=dashboard_service,
    )