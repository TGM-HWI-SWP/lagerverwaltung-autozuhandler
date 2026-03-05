# Startpunkt: verbindet Adapter + Service + GUI
from src.ui.app import run_gui
from src.domain.warehouse import Warehouse
from src.domain.product import Product



# --- Minimaler InMemory-Repo + Service (falls ihr schon eigene habt: sag Bescheid, dann passe ich es an) ---
class InMemoryRepository:
    def __init__(self):
        self._items = {}

    def add(self, product: Product):
        self._items[product.id] = product

    def list_all(self):
        return list(self._items.values())


class ProductService:
    def __init__(self, repo: InMemoryRepository, warehouse: Warehouse):
        self.repo = repo
        self.warehouse = warehouse

    def add_product(self, pid: str, name: str, desc: str, price: float, qty: int):
        p = Product(id=pid, name=name, description=desc, price=price, quantity=qty)
        # je nachdem wie euer Warehouse intern arbeitet:
        # - wenn es dict hat: warehouse.products[pid] = p
        # - wenn es add_product hat: warehouse.add_product(p)
        try:
            self.warehouse.add_product(p)
        except Exception:
            # fallback, falls Warehouse anders ist
            if hasattr(self.warehouse, "products") and isinstance(self.warehouse.products, dict):
                self.warehouse.products[p.id] = p
        self.repo.add(p)

    def list_products(self):
        return self.repo.list_all()


def main():
    print("Autozuhändler Lagerverwaltung gestartet")

    # Domain
    warehouse = Warehouse("Autohaus Lager")

    # Adapter
    repo = InMemoryRepository()

    # Service
    service = ProductService(repo, warehouse)

    # Export-Ordner (Nextcloud External Storage zeigt /mnt/exports -> Host-Ordner)
    export_dir = r"C:\Nextcloud_Autozu\exports"

    # GUI starten
    run_gui(service, export_dir)


if __name__ == "__main__":
    main()