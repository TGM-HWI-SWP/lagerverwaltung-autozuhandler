from src.adapters.memory_repositories import (
    InMemoryCarRepository,
    InMemoryCustomerRepository,
)
from src.services.car_service import CarService
from src.services.part_service import PartService
from src.services.customer_service import CustomerService
from src.services.dashboard_service import DashboardService
from src.services.filter_service import FilterService
from src.services.export_service import ExportService
from src.services.id_service import get_next_car_id, get_next_part_id, get_next_customer_id
from src.reports.car_reports import CarReport
from src.reports.part_reports import PartReport
from src.reports.customer_reports import CustomerReport
 
 
NEXTCLOUD_EXPORT_DIR = r"C:\Nextcloud_Autozu\exports"
 
car_repo = InMemoryCarRepository()
part_repo = InMemoryPartRepository()
customer_repo = InMemoryCustomerRepository()
 
car_service = CarService(car_repo, customer_repo)
part_service = PartService(part_repo)
customer_service = CustomerService(customer_repo, car_repo)
 
 
def get_customer_name_by_id(customer_id: str) -> str:
    if not customer_id:
        return "-"
    customer = customer_service.get_customer(customer_id)
    return customer.name if customer else "-"
 
 
dashboard_service = DashboardService(get_customer_name_by_id)
car_report = CarReport(get_customer_name_by_id)
part_report = PartReport()
customer_report = CustomerReport()
export_service = ExportService(NEXTCLOUD_EXPORT_DIR)
filter_service = FilterService(car_service, part_service, customer_service, get_customer_name_by_id)
 
 
def next_car_id():
    return get_next_car_id(car_repo)
 
 
def next_part_id():
    return get_next_part_id(part_repo)
 
 
def next_customer_id():
    return get_next_customer_id(customer_repo)