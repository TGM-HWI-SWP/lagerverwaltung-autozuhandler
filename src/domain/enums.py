from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    EMPLOYEE = "Mitarbeiter"
    TEACHER = "Lehrer"


class CarStatus(StrEnum):
    AVAILABLE = "Verfügbar"
    RESERVED = "Reserviert"
    SOLD = "Verkauft"


class PartStatus(StrEnum):
    AVAILABLE = "Verfügbar"
    REORDER = "Nachbestellen"
    UNAVAILABLE = "Nicht verfügbar"


class InvoiceStatus(StrEnum):
    OPEN = "Offen"
    PAID = "Bezahlt"
    CANCELED = "Storniert"


class FuelType(StrEnum):
    PETROL = "Benzin"
    DIESEL = "Diesel"
    HYBRID = "Hybrid"
    ELECTRIC = "Elektro"


CAR_STATUSES = [status.value for status in CarStatus]
PART_STATUSES = [status.value for status in PartStatus]
INVOICE_STATUSES = [status.value for status in InvoiceStatus]
FUELS = [fuel.value for fuel in FuelType]