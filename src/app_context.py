from __future__ import annotations
 
from dataclasses import dataclass

from pathlib import Path
 
from src.adapters.file_exporter import FileExporter

from src.adapters.memory_repositories import (

    InMemoryCarRepository,

    InMemoryCustomerRepository,

    InMemoryPartRepository,

)

from src.reports.car_reports import CarReportService

from src.reports.customer_reports import CustomerReportService

from src.reports.inventory_report import InventoryReportService

from src.reports.part_reports import PartReportService

from src.services.car_service import CarService

from src.services.customer_service import CustomerService

from src.services.dashboard_service import DashboardService

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
 
    car_report_service: CarReportService

    part_report_service: PartReportService

    customer_report_service: CustomerReportService

    inventory_report_service: InventoryReportService

    dashboard_service: DashboardService
 
 
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

    dashboard_service = DashboardService()
 
    return AppContext(

        car_repository=car_repository,

        part_repository=part_repository,

        customer_repository=customer_repository,

        exporter=exporter,

        car_service=car_service,

        part_service=part_service,

        customer_service=customer_service,

        car_report_service=car_report_service,

        part_report_service=part_report_service,

        customer_report_service=customer_report_service,

        inventory_report_service=inventory_report_service,

        dashboard_service=dashboard_service,

    )
 