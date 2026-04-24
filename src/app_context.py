from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from src.adapters.file_exporter import FileExporter
from src.adapters.memory_repositories import (
    InMemoryCustomerRepository,
    InMemoryMovementRepository,
    InMemoryPartRepository,
)
from src.adapters.mongo_repositories import MongoCarRepository
from src.reports.car_reports import CarReportService
from src.reports.customer_reports import CustomerReportService
from src.reports.inventory_report import InventoryReportService
from src.reports.movement_reports import MovementReportService
from src.reports.part_reports import PartReportService
from src.services.auth_service import AuthService
from src.services.car_service import CarService
from src.services.customer_service import CustomerService
from src.services.dashboard_service import DashboardService
from src.services.movement_service import MovementService
from src.services.part_service import PartService


APP_TITLE = "Autozuhändler"
NEXTCLOUD_EXPORT_DIR = Path(r"C:\Nextcloud_Autozu\exports")


@dataclass
class AppContext:
    car_repository: object
    part_repository: InMemoryPartRepository
    customer_repository: InMemoryCustomerRepository
    movement_repository: InMemoryMovementRepository
    exporter: FileExporter

    auth_service: AuthService
    movement_service: MovementService
    car_service: CarService
    part_service: PartService
    customer_service: CustomerService

    car_report_service: CarReportService
    part_report_service: PartReportService
    customer_report_service: CustomerReportService
    inventory_report_service: InventoryReportService
    movement_report_service: MovementReportService
    dashboard_service: DashboardService


def build_app_context() -> AppContext:
    use_mongodb = os.getenv("USE_MONGODB", "false").lower() == "true"
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db_name = os.getenv("MONGO_DB_NAME", "autozuhaendler")

    if use_mongodb:
        car_repository = MongoCarRepository(
            mongo_uri=mongo_uri,
            database_name=mongo_db_name,
            collection_name="cars",
        )
    else:
        from src.adapters.memory_repositories import InMemoryCarRepository
        car_repository = InMemoryCarRepository()

    part_repository = InMemoryPartRepository()
    customer_repository = InMemoryCustomerRepository()
    movement_repository = InMemoryMovementRepository()
    exporter = FileExporter(NEXTCLOUD_EXPORT_DIR)

    auth_service = AuthService()
    movement_service = MovementService(movement_repository)

    car_service = CarService(
        car_repository=car_repository,
        customer_repository=customer_repository,
        movement_service=movement_service,
    )
    part_service = PartService(
        part_repository=part_repository,
        movement_service=movement_service,
    )
    customer_service = CustomerService(
        customer_repository=customer_repository,
        car_repository=car_repository,
        movement_service=movement_service,
    )

    car_report_service = CarReportService(
        car_repository=car_repository,
        customer_repository=customer_repository,
    )
    part_report_service = PartReportService(
        part_repository=part_repository,
    )
    customer_report_service = CustomerReportService(
        customer_repository=customer_repository,
    )
    inventory_report_service = InventoryReportService(
        part_repository=part_repository,
    )
    movement_report_service = MovementReportService(
        movement_repository=movement_repository,
    )
    dashboard_service = DashboardService()

    return AppContext(
        car_repository=car_repository,
        part_repository=part_repository,
        customer_repository=customer_repository,
        movement_repository=movement_repository,
        exporter=exporter,
        auth_service=auth_service,
        movement_service=movement_service,
        car_service=car_service,
        part_service=part_service,
        customer_service=customer_service,
        car_report_service=car_report_service,
        part_report_service=part_report_service,
        customer_report_service=customer_report_service,
        inventory_report_service=inventory_report_service,
        movement_report_service=movement_report_service,
        dashboard_service=dashboard_service,
    )