from __future__ import annotations

from dataclasses import dataclass

from domain.enums import UserRole
from services.formatting_service import safe_str


@dataclass(frozen=True)
class Employee:
    username: str
    password: str
    role: UserRole
    name: str


class AuthService:
    def __init__(self) -> None:
        self._employees: dict[str, Employee] = {
            "Julian": Employee("Julian", "admin123", UserRole.ADMIN, "Julian"),
            "Fabienne": Employee("Fabienne", "admin456", UserRole.ADMIN, "Fabienne"),
            "Mikail": Employee("Mikail", "admin789", UserRole.ADMIN, "Miki"),
            "Sirin": Employee("Sirin", "admin000", UserRole.ADMIN, "Sirin"),
            "verkauf": Employee("verkauf", "verkauf123", UserRole.EMPLOYEE, "Max Verkauf"),
            "lager": Employee("lager", "lager123", UserRole.EMPLOYEE, "Lena Lager"),
            "lehrer": Employee("lehrer", "lehrer123", UserRole.TEACHER, "Schobi Ratschi"),
        }

    def login(self, username: str, password: str) -> Employee:
        username = safe_str(username)
        password = safe_str(password)

        if username not in self._employees:
            raise ValueError("Unbekannter Benutzer.")

        employee = self._employees[username]
        if password != employee.password:
            raise ValueError("Falsches Passwort.")

        return employee