from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.adapters.file_exporter import FileExporter
from src.adapters.memory_repositories import (
    InMemoryCarRepository,
    InMemoryCustomerRepository,
    InMemoryPartRepository,
)

APP_TITLE = "Autozuhändler"
NEXTCLOUD_EXPORT_DIR = Path(r"C:\Nextcloud_Autozu\exports")


@dataclass
class AppContext:
    car_repository: InMemoryCarRepository
    part_repository: InMemoryPartRepository
    customer_repository: InMemoryCustomerRepository
    exporter: FileExporter


def build_app_context() -> AppContext:
    car_repository = InMemoryCarRepository()
    part_repository = InMemoryPartRepository()
    customer_repository = InMemoryCustomerRepository()
    exporter = FileExporter(NEXTCLOUD_EXPORT_DIR)

    return AppContext(
        car_repository=car_repository,
        part_repository=part_repository,
        customer_repository=customer_repository,
        exporter=exporter,
    )