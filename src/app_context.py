from __future__ import annotations
 
from dataclasses import dataclass
from pathlib import Path
 
from src.adapters.file_exporter import FileExporter
from src.adapters.memory_repositories import (
    InMemoryCarRepository,
    InMemoryCustomerRepository,
    InMemoryPartRepository,
)
from src.reports.inventory_report import InventoryReportService
from src.services.car_service import CarService
from src.services.customer_service import CustomerService
from src.services.part_service import PartService
 
APP_TITLE = "Autozuhändler"
NEXTCLOUD_EXPORT_DIR = Path(r"C:\Nextcloud_Autozu\exports")
 
 
@dataclass
class AppContext:
    car_repository: InMemoryCarRepository
    part_repository: InMemoryPartRepository
    customer_repository: InMemoryCustomerRepository
    exporter: FileExporter
 
    car_service: CarService
    part_service: PartService
    customer_service: CustomerService
 
    inventory_report_service: InventoryReportService
 
 
def build_app_context() -> AppContext:
    car_repository = InMemoryCarRepository()
    part_repository = InMemoryPartRepository()
    customer_repository = InMemoryCustomerRepository()
    exporter = FileExporter(NEXTCLOUD_EXPORT_DIR)
 
    car_service = CarService(
        car_repository=car_repository,
        customer_repository=customer_repository,
    )
    part_service = PartService(
        part_repository=part_repository,
    )
    customer_service = CustomerService(
        customer_repository=customer_repository,
        car_repository=car_repository,
    )
 
    inventory_report_service = InventoryReportService(
        part_repository=part_repository,
    )
 
    return AppContext(
        car_repository=car_repository,
        part_repository=part_repository,
        customer_repository=customer_repository,
        exporter=exporter,
        car_service=car_service,
        part_service=part_service,
        customer_service=customer_service,
        inventory_report_service=inventory_report_service,
    )