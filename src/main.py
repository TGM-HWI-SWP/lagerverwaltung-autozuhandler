from __future__ import annotations
 
from src.app_context import APP_TITLE, build_app_context
 
 
def run() -> None:
    app_context = build_app_context()
    print(f"{APP_TITLE} – Basisarchitektur geladen.")
    print("Repositories und Export-Adapter sind initialisiert.")
    print("GUI und Services werden durch Person 2, 3 und 4 ergänzt.")
    print(app_context)
 
 
if __name__ == "__main__":
    run()