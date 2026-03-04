from domain.warehouse import Warehouse
from domain.product import Product
from pathlib import Path
from datetime import datetime

print("Autozuhändler Lagerverwaltung gestartet")

# Lager erstellen
warehouse = Warehouse("Autohaus Lager")

# Produkt erstellen (ALLE Felder!)
product = Product(
    id="A001",
    name="Reifen Set",
    description="Winterreifen Set für PKW",
    price=299.99,
    quantity=10
)

warehouse.add_product(product)

print("Produkt hinzugefügt:", product.name)

# -----------------------------
# Report erstellen
# -----------------------------

report_text = f"""
Autozuhändler Lager Report
--------------------------
Datum: {datetime.now()}

Lager: {warehouse.name}

Produkte im Lager:
"""

for p in warehouse.products.values():
    report_text += f"- {p.name} | Menge: {p.quantity} | Preis: {p.price}\n"

# -----------------------------
# Nextcloud Export
# -----------------------------

export_folder = Path(r"C:\Nextcloud_Autozu\exports")
export_folder.mkdir(parents=True, exist_ok=True)

report_file = export_folder / "lager_report.txt"

with open(report_file, "w", encoding="utf-8") as f:
    f.write(report_text)

print("Report gespeichert unter:", report_file)

print("Programm beendet")