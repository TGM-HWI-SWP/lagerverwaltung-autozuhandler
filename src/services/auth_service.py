from __future__ import annotations

from src.services.formatting_service import safe_str
from src.services.service_result import ServiceResult


class AuthService:
    def __init__(self) -> None:
        self._employees = {
            "Julian": {"password": "admin123", "role": "Admin", "name": "Julian"},
            "Fabienne": {"password": "admin456", "role": "Admin", "name": "Fabienne"},
            "Mikail": {"password": "admin789", "role": "Admin", "name": "Mikail"},
            "Sirin": {"password": "admin000", "role": "Admin", "name": "Sirin"},
            "verkauf": {"password": "verkauf123", "role": "Mitarbeiter", "name": "Max Verkauf"},
            "lager": {"password": "lager123", "role": "Mitarbeiter", "name": "Lena Lager"},
            "lehrer": {"password": "lehrer123", "role": "Lehrer", "name": "Schobi Ratschi"},
        }

    def login(self, username: object, password: object) -> ServiceResult:
        prepared_username = safe_str(username)
        prepared_password = safe_str(password)

        if prepared_username not in self._employees:
            return ServiceResult.fail("Unbekannter Benutzer.")

        user = self._employees[prepared_username]
        if prepared_password != user["password"]:
            return ServiceResult.fail("Falsches Passwort.")

        return ServiceResult.ok(
            f"Angemeldet als {user['name']} ({user['role']})",
            name=user["name"],
            role=user["role"],
            username=prepared_username,
        )

    def logout(self) -> ServiceResult:
        return ServiceResult.ok("Abgemeldet.")

    def get_demo_logins(self) -> list[str]:
        return [
            "Julian / admin123",
            "Fabienne / admin456",
            "Mikail / admin789",
            "Sirin / admin000",
            "verkauf / verkauf123",
            "lager / lager123",
            "lehrer / lehrer123",
        ]