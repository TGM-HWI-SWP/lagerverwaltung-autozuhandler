import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime


def run_gui(service, export_dir: str):
    """
    GUI darf nur den Service benutzen.
    Export wird als Textdatei in export_dir gespeichert (z.B. Nextcloud exports).
    """
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)

    root = tk.Tk()
    root.title("Autozuhändler Lagerverwaltung")
    root.geometry("650x420")

    # --- UI Elements ---
    title = tk.Label(root, text="Autozuhändler System", font=("Arial", 18))
    title.pack(pady=10)

    form = tk.Frame(root)
    form.pack(pady=5)

    tk.Label(form, text="ID").grid(row=0, column=0, sticky="e")
    entry_id = tk.Entry(form, width=30)
    entry_id.grid(row=0, column=1, padx=5, pady=3)

    tk.Label(form, text="Name").grid(row=1, column=0, sticky="e")
    entry_name = tk.Entry(form, width=30)
    entry_name.grid(row=1, column=1, padx=5, pady=3)

    tk.Label(form, text="Beschreibung").grid(row=2, column=0, sticky="e")
    entry_desc = tk.Entry(form, width=30)
    entry_desc.grid(row=2, column=1, padx=5, pady=3)

    tk.Label(form, text="Preis").grid(row=3, column=0, sticky="e")
    entry_price = tk.Entry(form, width=30)
    entry_price.grid(row=3, column=1, padx=5, pady=3)

    tk.Label(form, text="Menge").grid(row=4, column=0, sticky="e")
    entry_qty = tk.Entry(form, width=30)
    entry_qty.grid(row=4, column=1, padx=5, pady=3)

    listbox = tk.Listbox(root, width=90, height=10)
    listbox.pack(pady=10)

    status = tk.Label(root, text="", anchor="w")
    status.pack(fill="x", padx=10)

    def refresh_list():
        listbox.delete(0, tk.END)
        for p in service.list_products():
            listbox.insert(tk.END, f"{p.id} | {p.name} | {p.description} | {p.price} EUR | Menge: {p.quantity}")

    def add_product():
        try:
            pid = entry_id.get().strip()
            name = entry_name.get().strip()
            desc = entry_desc.get().strip()
            price = float(entry_price.get().strip())
            qty = int(entry_qty.get().strip())

            if not pid or not name:
                messagebox.showwarning("Fehler", "Bitte mindestens ID und Name eingeben.")
                return

            service.add_product(pid, name, desc, price, qty)
            refresh_list()

            entry_id.delete(0, tk.END)
            entry_name.delete(0, tk.END)
            entry_desc.delete(0, tk.END)
            entry_price.delete(0, tk.END)
            entry_qty.delete(0, tk.END)

            status.config(text=f"Produkt {pid} hinzugefügt.")
        except ValueError:
            messagebox.showerror("Fehler", "Preis muss Zahl sein und Menge eine ganze Zahl.")

    def export_report():
        products = list(service.list_products())
        if not products:
            messagebox.showinfo("Report", "Keine Produkte vorhanden.")
            return

        total_value = sum(p.price * p.quantity for p in products)

        report_text = (
            "Autozuhändler – Lager Report\n"
            "---------------------------\n"
            f"Datum: {datetime.now()}\n\n"
            "Produkte:\n"
        )
        for p in products:
            report_text += f"- {p.id}: {p.name} | Menge {p.quantity} | {p.price} EUR | Wert {p.price * p.quantity} EUR\n"

        report_text += f"\nGesamtwert Lager: {total_value} EUR\n"

        filename = f"lager_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        out_file = export_path / filename
        out_file.write_text(report_text, encoding="utf-8")

        messagebox.showinfo("Report exportiert", f"Gespeichert: {out_file}")
        status.config(text=f"Report exportiert: {filename}")

    btns = tk.Frame(root)
    btns.pack(pady=5)

    tk.Button(btns, text="Produkt hinzufügen", command=add_product, width=20).grid(row=0, column=0, padx=5)
    tk.Button(btns, text="Liste aktualisieren", command=refresh_list, width=20).grid(row=0, column=1, padx=5)
    tk.Button(btns, text="Report exportieren", command=export_report, width=20).grid(row=0, column=2, padx=5)

    refresh_list()
    root.mainloop()