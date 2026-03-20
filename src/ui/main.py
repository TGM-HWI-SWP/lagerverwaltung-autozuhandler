from __future__ import annotations

import gradio as gr

from src.app_context import APP_TITLE, AppContext
from src.services.car_service import CAR_STATUSES, FUELS, INVOICE_STATUSES
from src.services.formatting_service import safe_str, smart_capitalize
from src.services.part_service import PART_STATUSES
from src.ui.charts import (
    get_car_status_chart,
    get_customer_chart,
    get_part_status_chart,
    get_profit_trend_chart,
)
from src.ui.ui_helpers import (
    extract_customer_id,
    get_brand_choices,
    get_car_id_choices,
    get_category_choices,
    get_customer_choice_by_id,
    get_customer_choices,
    get_customer_id_choices,
    get_part_id_choices,
    make_choice_suggestions,
)


def create_ui(app: AppContext) -> gr.Blocks:
    def car_df(data: list[dict] | None = None):
        return app.car_report_service.generate_dataframe(data)

    def part_df(data: list[dict] | None = None):
        return app.part_report_service.generate_dataframe(data)

    def customer_df(data: list[dict] | None = None):
        return app.customer_report_service.generate_dataframe(data)

    def car_report_text(data: list[dict] | None = None) -> str:
        return app.car_report_service.generate_text_report(data)

    def part_report_text(data: list[dict] | None = None) -> str:
        return app.part_report_service.generate_text_report(data)

    def customer_report_text(data: list[dict] | None = None) -> str:
        return app.customer_report_service.generate_text_report(data)

    def inventory_report_text(data: list[dict] | None = None) -> str:
        return app.inventory_report_service.generate_text_report(data)

    def get_car_cards(data: list[dict] | None = None):
        stats = app.car_report_service.get_stats(data)
        return app.dashboard_service.get_car_dashboard_cards(*stats)

    def get_part_cards(data: list[dict] | None = None):
        stats = app.part_report_service.get_stats(data)
        return app.dashboard_service.get_part_dashboard_cards(*stats)

    def get_customer_cards(data: list[dict] | None = None):
        stats = app.customer_report_service.get_stats(data)
        return app.dashboard_service.get_customer_dashboard_cards(*stats)

    def clear_car_form():
        return (
            app.car_service.get_next_id(),
            "",
            "",
            "",
            "",
            None,
            "",
            "",
            "",
            "-",
            "Offen",
            None,
        )

    def clear_part_form():
        return (
            app.part_service.get_next_id(),
            "",
            "",
            "",
            "",
            "",
            None,
        )

    def clear_customer_form():
        return (
            app.customer_service.get_next_id(),
            "",
            "",
            "",
            "",
        )

    def refresh_car_full(data: list[dict] | None = None, message: str = ""):
        source = data if data is not None else app.car_service.get_all()
        customers = app.customer_service.get_all()
        return (
            message,
            car_df(source),
            car_report_text(source) if source else "Keine passenden Fahrzeuge gefunden.",
            *get_car_cards(source),
            get_car_status_chart(source),
            get_profit_trend_chart(source),
            gr.update(choices=["Alle"] + get_brand_choices(app.car_service.get_all()), value="Alle"),
            gr.update(choices=get_car_id_choices(app.car_service.get_all()), value=None),
            gr.update(choices=get_customer_choices(customers), value="-"),
            app.car_service.get_next_id(),
        )

    def refresh_part_full(data: list[dict] | None = None, message: str = ""):
        source = data if data is not None else app.part_service.get_all()
        return (
            message,
            part_df(source),
            part_report_text(source) if source else "Keine passenden Teile gefunden.",
            inventory_report_text(source) if source else "Keine passenden Teile gefunden.",
            *get_part_cards(source),
            get_part_status_chart(source),
            gr.update(choices=["Alle"] + get_category_choices(app.part_service.get_all()), value="Alle"),
            gr.update(choices=get_part_id_choices(app.part_service.get_all()), value=None),
            app.part_service.get_next_id(),
        )

    def refresh_customer_full(data: list[dict] | None = None, message: str = ""):
        source = data if data is not None else app.customer_service.get_all()
        customers_all = app.customer_service.get_all()
        return (
            message,
            customer_df(source),
            customer_report_text(source) if source else "Keine passenden Kunden gefunden.",
            *get_customer_cards(source),
            get_customer_chart(source),
            gr.update(choices=get_customer_id_choices(customers_all), value=None),
            gr.update(choices=get_customer_choices(customers_all), value="-"),
            app.customer_service.get_next_id(),
        )

    def initial_load():
        return (
            *get_car_cards(),
            car_df(),
            car_report_text(),
            get_car_status_chart(),
            get_profit_trend_chart(),
            gr.update(choices=["Alle"] + get_brand_choices(app.car_service.get_all()), value="Alle"),
            gr.update(choices=get_car_id_choices(app.car_service.get_all()), value=None),
            gr.update(choices=get_customer_choices(app.customer_service.get_all()), value="-"),
            app.car_service.get_next_id(),

            *get_part_cards(),
            part_df(),
            part_report_text(),
            inventory_report_text(),
            get_part_status_chart(),
            gr.update(choices=["Alle"] + get_category_choices(app.part_service.get_all()), value="Alle"),
            gr.update(choices=get_part_id_choices(app.part_service.get_all()), value=None),
            app.part_service.get_next_id(),

            *get_customer_cards(),
            customer_df(),
            customer_report_text(),
            get_customer_chart(),
            gr.update(choices=get_customer_id_choices(app.customer_service.get_all()), value=None),
            app.customer_service.get_next_id(),
        )

    def login_user(username: str, password: str):
        result = app.auth_service.login(username, password)
        if not result.success:
            return (
                result.message,
                gr.update(visible=True),
                gr.update(visible=False),
                "",
                "",
            )

        return (
            result.message,
            gr.update(visible=False),
            gr.update(visible=True),
            result.data["name"],
            result.data["role"],
        )

    def logout_user():
        result = app.auth_service.logout()
        return (
            result.message,
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            "",
        )

    def load_car_for_edit(selected_id: str):
        car = app.car_service.get_by_id(selected_id)
        if not car:
            return "", "", "", "", "", None, "", "", "", "-", "Offen", None, "Fahrzeug nicht gefunden."

        customers = app.customer_service.get_all()
        return (
            car["id"],
            car["brand"],
            car["model"],
            str(car["year"]),
            str(car["mileage"]),
            car["fuel"],
            car["color"],
            str(car["purchase_price"]),
            str(car["sale_price"]),
            get_customer_choice_by_id(customers, car.get("customer_id", "")),
            car["invoice_status"],
            car["status"],
            f"Fahrzeug '{car['id']}' geladen.",
        )

    def add_car(car_id, brand, model, year, mileage, fuel, color, purchase_price, sale_price, customer_choice, invoice_status, status):
        result = app.car_service.create_car(
            car_id=car_id,
            brand=brand,
            model=model,
            year=year,
            mileage=mileage,
            fuel=fuel,
            color=color,
            purchase_price=purchase_price,
            sale_price=sale_price,
            customer_id=extract_customer_id(customer_choice),
            invoice_status=invoice_status,
            status=status,
        )

        if not result.success:
            return (
                *refresh_car_full(message=result.message),
                car_id, brand, model, year, mileage, fuel, color, purchase_price, sale_price, customer_choice, invoice_status, status
            )

        return (
            *refresh_car_full(message=result.message),
            *clear_car_form()
        )

    def update_car(selected_id, car_id, brand, model, year, mileage, fuel, color, purchase_price, sale_price, customer_choice, invoice_status, status):
        result = app.car_service.update_car(
            selected_id=selected_id,
            car_id=car_id,
            brand=brand,
            model=model,
            year=year,
            mileage=mileage,
            fuel=fuel,
            color=color,
            purchase_price=purchase_price,
            sale_price=sale_price,
            customer_id=extract_customer_id(customer_choice),
            invoice_status=invoice_status,
            status=status,
        )

        if not result.success:
            return (
                *refresh_car_full(message=result.message),
                car_id, brand, model, year, mileage, fuel, color, purchase_price, sale_price, customer_choice, invoice_status, status
            )

        updated = result.data["car"]
        customers = app.customer_service.get_all()
        return (
            *refresh_car_full(message=result.message),
            updated["id"],
            updated["brand"],
            updated["model"],
            str(updated["year"]),
            str(updated["mileage"]),
            updated["fuel"],
            updated["color"],
            str(updated["purchase_price"]),
            str(updated["sale_price"]),
            get_customer_choice_by_id(customers, updated.get("customer_id", "")),
            updated["invoice_status"],
            updated["status"],
        )

    def delete_car(selected_id: str):
        result = app.car_service.delete_car(selected_id)
        return (
            *refresh_car_full(message=result.message),
            *clear_car_form()
        )

    def filter_cars(search_term: str, brand_filter: str, status_filter: str):
        filtered = app.car_service.filter_cars(search_term, brand_filter, status_filter)
        return (
            car_df(filtered),
            car_report_text(filtered) if filtered else "Keine passenden Fahrzeuge gefunden.",
            *get_car_cards(filtered),
            get_car_status_chart(filtered),
            get_profit_trend_chart(filtered),
        )

    def reset_cars():
        return (
            "",
            "Alle",
            "Alle",
            car_df(),
            car_report_text(),
            *get_car_cards(),
            get_car_status_chart(),
            get_profit_trend_chart(),
        )

    def export_cars_txt():
        return app.exporter.export_text("fahrzeugreport", app.car_report_service.generate_text_report())

    def export_cars_csv():
        return app.exporter.export_csv(app.car_report_service.generate_dataframe(), "fahrzeuge")

    def export_cars_excel():
        return app.exporter.export_excel(app.car_report_service.generate_dataframe(), "fahrzeuge")

    def load_part_for_edit(selected_id: str):
        part = app.part_service.get_by_id(selected_id)
        if not part:
            return "", "", "", "", "", "", None, "Teil nicht gefunden."

        return (
            part["id"],
            part["name"],
            part["category"],
            part["brand"],
            str(part["price"]),
            str(part["stock"]),
            part["status"],
            f"Teil '{part['id']}' geladen.",
        )

    def add_part(part_id, name, category, brand, price, stock, status):
        result = app.part_service.create_part(
            part_id=part_id,
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            status=status,
        )

        if not result.success:
            return (
                *refresh_part_full(message=result.message),
                part_id, name, category, brand, price, stock, status
            )

        return (
            *refresh_part_full(message=result.message),
            *clear_part_form()
        )

    def update_part(selected_id, part_id, name, category, brand, price, stock, status):
        result = app.part_service.update_part(
            selected_id=selected_id,
            part_id=part_id,
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            status=status,
        )

        if not result.success:
            return (
                *refresh_part_full(message=result.message),
                part_id, name, category, brand, price, stock, status
            )

        updated = result.data["part"]
        return (
            *refresh_part_full(message=result.message),
            updated["id"],
            updated["name"],
            updated["category"],
            updated["brand"],
            str(updated["price"]),
            str(updated["stock"]),
            updated["status"],
        )

    def delete_part(selected_id: str):
        result = app.part_service.delete_part(selected_id)
        return (
            *refresh_part_full(message=result.message),
            *clear_part_form()
        )

    def filter_parts(search_term: str, category_filter: str, status_filter: str):
        filtered = app.part_service.filter_parts(search_term, category_filter, status_filter)
        return (
            part_df(filtered),
            part_report_text(filtered) if filtered else "Keine passenden Teile gefunden.",
            *get_part_cards(filtered),
            get_part_status_chart(filtered),
            inventory_report_text(filtered) if filtered else "Keine passenden Teile gefunden.",
        )

    def reset_parts():
        return (
            "",
            "Alle",
            "Alle",
            part_df(),
            part_report_text(),
            *get_part_cards(),
            get_part_status_chart(),
            inventory_report_text(),
        )

    def export_parts_txt():
        return app.exporter.export_text("teile_report", app.part_report_service.generate_text_report())

    def export_parts_csv():
        return app.exporter.export_csv(app.part_report_service.generate_dataframe(), "teile")

    def export_parts_excel():
        return app.exporter.export_excel(app.part_report_service.generate_dataframe(), "teile")

    def load_customer_for_edit(selected_id: str):
        customer = app.customer_service.get_by_id(selected_id)
        if not customer:
            return "", "", "", "", "", "Kunde nicht gefunden."

        return (
            customer["id"],
            customer["name"],
            customer["phone"],
            customer["email"],
            customer["address"],
            f"Kunde '{customer['id']}' geladen.",
        )

    def add_customer(customer_id, name, phone, email, address):
        result = app.customer_service.create_customer(
            customer_id=customer_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
        )

        if not result.success:
            return (
                *refresh_customer_full(message=result.message),
                customer_id, name, phone, email, address
            )

        return (
            *refresh_customer_full(message=result.message),
            *clear_customer_form()
        )

    def update_customer(selected_id, customer_id, name, phone, email, address):
        result = app.customer_service.update_customer(
            selected_id=selected_id,
            customer_id=customer_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
        )

        if not result.success:
            return (
                *refresh_customer_full(message=result.message),
                customer_id, name, phone, email, address
            )

        updated = result.data["customer"]
        return (
            *refresh_customer_full(message=result.message),
            updated["id"],
            updated["name"],
            updated["phone"],
            updated["email"],
            updated["address"],
        )

    def delete_customer(selected_id: str):
        result = app.customer_service.delete_customer(selected_id)
        return (
            *refresh_customer_full(message=result.message),
            *clear_customer_form()
        )

    def filter_customers(search_term: str):
        filtered = app.customer_service.filter_customers(search_term)
        return (
            customer_df(filtered),
            customer_report_text(filtered) if filtered else "Keine passenden Kunden gefunden.",
            *get_customer_cards(filtered),
            get_customer_chart(filtered),
        )

    def reset_customers():
        return (
            "",
            customer_df(),
            customer_report_text(),
            *get_customer_cards(),
            get_customer_chart(),
        )

    def export_customers_txt():
        return app.exporter.export_text("kunden_report", app.customer_report_service.generate_text_report())

    def export_customers_csv():
        return app.exporter.export_csv(app.customer_report_service.generate_dataframe(), "kunden")

    def export_customers_excel():
        return app.exporter.export_excel(app.customer_report_service.generate_dataframe(), "kunden")

    def suggest_brand_choices(search_text: str):
        return gr.update(choices=make_choice_suggestions(search_text, get_brand_choices(app.car_service.get_all())), value=None)

    def suggest_category_choices(search_text: str):
        return gr.update(choices=make_choice_suggestions(search_text, get_category_choices(app.part_service.get_all())), value=None)

    def pick_dropdown_value(value: str):
        return value or ""

    with gr.Blocks(title=APP_TITLE, elem_id="dashboard-root") as demo:
        current_user_name = gr.State("")
        current_user_role = gr.State("")

        login_container = gr.Column(visible=True)
        app_container = gr.Column(visible=False)

        with login_container:
            gr.HTML(
                """
                <div class="main-title">
                    <h1>Autozuhändler</h1>
                    <p>Moderne Verwaltung für Fahrzeuge, Lagerteile, Kunden, Berichte und Exporte.</p>
                </div>
                """
            )
            with gr.Row():
                with gr.Column(scale=1):
                    login_username = gr.Textbox(label="Benutzername")
                    login_password = gr.Textbox(label="Passwort", type="password")
                    login_btn = gr.Button("Anmelden", variant="primary", elem_classes=["primary-btn"])
                    login_status = gr.Textbox(label="Status", interactive=False)
                with gr.Column(scale=1):
                    demo_logins = "<br>".join(app.auth_service.get_demo_logins())
                    gr.HTML(f"""
                    <div class="legend-box">
                        <b>Demo-Zugänge</b><br><br>
                        {demo_logins}
                    </div>
                    """)

        with app_container:
            gr.HTML(
                """
                <div class="main-title">
                    <h1>Autozuhändler</h1>
                    <p>Verwaltung von Fahrzeugen, Teilen, Kunden, Rechnungsstatus, Reports und Exporten.</p>
                </div>
                """
            )

            with gr.Row():
                user_info = gr.Textbox(label="Angemeldeter Mitarbeiter", interactive=False)
                user_role = gr.Textbox(label="Rolle", interactive=False)
                logout_btn = gr.Button("Abmelden", elem_classes=["secondary-btn"])

            with gr.Tab("Fahrzeuge"):
                with gr.Row():
                    car_kpi_1 = gr.HTML()
                    car_kpi_2 = gr.HTML()
                    car_kpi_3 = gr.HTML()
                    car_kpi_4 = gr.HTML()
                    car_kpi_5 = gr.HTML()

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">🚘 Fahrzeug anlegen / bearbeiten</div><div class="subtle-text">Automatische ID, Verkauf, Kunde, Rechnungsstatus und Statusverwaltung.</div>')

                        car_edit_select = gr.Dropdown(label="Fahrzeug wählen", choices=[], value=None)
                        with gr.Row():
                            car_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                            car_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                        car_id = gr.Textbox(label="Fahrzeug-ID", interactive=False, value=app.car_service.get_next_id())
                        car_brand = gr.Textbox(label="Marke")
                        car_brand_suggestions = gr.Dropdown(label="Marken-Vorschläge", choices=[], value=None)
                        car_model = gr.Textbox(label="Modell")
                        car_year = gr.Textbox(label="Baujahr")
                        car_mileage = gr.Textbox(label="Kilometerstand")
                        car_fuel = gr.Dropdown(choices=FUELS, label="Kraftstoff", value=None)
                        car_color = gr.Textbox(label="Farbe")
                        car_purchase_price = gr.Textbox(label="Ankaufspreis")
                        car_sale_price = gr.Textbox(label="Verkaufspreis")
                        car_customer = gr.Dropdown(label="Kunde", choices=get_customer_choices(app.customer_service.get_all()), value="-")
                        car_invoice_status = gr.Dropdown(choices=INVOICE_STATUSES, label="Rechnungsstatus", value="Offen")
                        car_status = gr.Dropdown(choices=CAR_STATUSES, label="Status", value=None)

                        with gr.Row():
                            car_add_btn = gr.Button("Neues Fahrzeug speichern", elem_classes=["primary-btn"])
                            car_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                            car_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                        car_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                    with gr.Column(scale=2):
                        gr.HTML('<div class="section-title">📋 Fahrzeugbestand</div><div class="subtle-text">Suche nach ID, Marke, Modell, Kunde und Status.</div>')
                        car_table = gr.Dataframe(interactive=False, label="Fahrzeugbestand")

                with gr.Row():
                    car_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Marke, Modell, Kunde, Status")
                    car_brand_filter = gr.Dropdown(label="🏷️ Marke filtern", choices=["Alle"], value="Alle", filterable=True)
                    car_status_filter = gr.Dropdown(label="📌 Status filtern", choices=["Alle"] + CAR_STATUSES, value="Alle")

                with gr.Row():
                    car_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                    car_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">🧾 Fahrzeugreport</div>')
                        car_report = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">📊 Auswertung Fahrzeuge</div>')
                        car_chart = gr.Plot(label="Fahrzeuge pro Status")
                        car_profit_chart = gr.Plot(label="Gewinn pro verkauftem Fahrzeug")

                with gr.Row():
                    car_export_txt_btn = gr.Button("TXT exportieren", elem_classes=["primary-btn"])
                    car_export_csv_btn = gr.Button("CSV exportieren", elem_classes=["secondary-btn"])
                    car_export_xlsx_btn = gr.Button("Excel exportieren", elem_classes=["secondary-btn"])
                car_export_status = gr.Textbox(label="Exportstatus", interactive=False)

            with gr.Tab("Teile"):
                with gr.Row():
                    part_kpi_1 = gr.HTML()
                    part_kpi_2 = gr.HTML()
                    part_kpi_3 = gr.HTML()
                    part_kpi_4 = gr.HTML()

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">📦 Teil anlegen / bearbeiten</div><div class="subtle-text">Mit Lagerwert, Bestand und Ampel-Status.</div>')

                        part_edit_select = gr.Dropdown(label="Teil wählen", choices=[], value=None)
                        with gr.Row():
                            part_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                            part_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                        part_id = gr.Textbox(label="Teile-ID", interactive=False, value=app.part_service.get_next_id())
                        part_name = gr.Textbox(label="Teilename")
                        part_category = gr.Textbox(label="Kategorie")
                        part_category_suggestions = gr.Dropdown(label="Kategorie-Vorschläge", choices=[], value=None)
                        part_brand = gr.Textbox(label="Marke / Hersteller")
                        part_price = gr.Textbox(label="Preis")
                        part_stock = gr.Textbox(label="Bestand")
                        part_status = gr.Dropdown(choices=PART_STATUSES, label="Lagerstatus", value=None)

                        gr.HTML(
                            """
                            <div class="legend-box">
                                <b>Ampelstatus</b><br>
                                🟢 Verfügbar<br>
                                🟡 Nachbestellen<br>
                                🔴 Nicht verfügbar
                            </div>
                            """
                        )

                        with gr.Row():
                            part_add_btn = gr.Button("Neues Teil speichern", elem_classes=["primary-btn"])
                            part_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                            part_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                        part_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                    with gr.Column(scale=2):
                        gr.HTML('<div class="section-title">🗂️ Teilelager</div><div class="subtle-text">Bestand, Lagerwert, Statuserkennung und Reports.</div>')
                        part_table = gr.Dataframe(interactive=False, label="Teilebestand")

                with gr.Row():
                    part_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Name, Kategorie, Marke, Status")
                    part_category_filter = gr.Dropdown(label="🏷️ Kategorie filtern", choices=["Alle"], value="Alle", filterable=True)
                    part_status_filter = gr.Dropdown(label="📌 Status filtern", choices=["Alle"] + PART_STATUSES, value="Alle")

                with gr.Row():
                    part_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                    part_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">🧾 Teile-Report</div>')
                        part_report = gr.Textbox(label="Report", lines=14, interactive=False, elem_classes=["report-box"])
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">📦 Lagerstandsreport</div>')
                        inventory_report = gr.Textbox(label="Lagerreport", lines=14, interactive=False, elem_classes=["report-box"])

                with gr.Row():
                    part_chart = gr.Plot(label="Teilebestand nach Status")

                with gr.Row():
                    part_export_txt_btn = gr.Button("TXT exportieren", elem_classes=["primary-btn"])
                    part_export_csv_btn = gr.Button("CSV exportieren", elem_classes=["secondary-btn"])
                    part_export_xlsx_btn = gr.Button("Excel exportieren", elem_classes=["secondary-btn"])
                part_export_status = gr.Textbox(label="Exportstatus", interactive=False)

            with gr.Tab("Kunden"):
                with gr.Row():
                    customer_kpi_1 = gr.HTML()
                    customer_kpi_2 = gr.HTML()
                    customer_kpi_3 = gr.HTML()

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">👤 Kunde anlegen / bearbeiten</div><div class="subtle-text">Mit Kontaktübersicht und Löschschutz bei Verknüpfungen.</div>')

                        customer_edit_select = gr.Dropdown(label="Kunde wählen", choices=[], value=None)
                        with gr.Row():
                            customer_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                            customer_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                        customer_id = gr.Textbox(label="Kunden-ID", interactive=False, value=app.customer_service.get_next_id())
                        customer_name = gr.Textbox(label="Name")
                        customer_phone = gr.Textbox(label="Telefon")
                        customer_email = gr.Textbox(label="E-Mail")
                        customer_address = gr.Textbox(label="Adresse", lines=3)

                        with gr.Row():
                            customer_add_btn = gr.Button("Neuen Kunden speichern", elem_classes=["primary-btn"])
                            customer_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                            customer_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                        customer_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                    with gr.Column(scale=2):
                        gr.HTML('<div class="section-title">👥 Kundenverwaltung</div><div class="subtle-text">Alle Kunden mit Kontaktübersicht und Statistik.</div>')
                        customer_table = gr.Dataframe(interactive=False, label="Kunden")

                with gr.Row():
                    customer_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Name, Telefon, E-Mail, Adresse")
                    customer_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                    customer_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">🧾 Kundenreport</div>')
                        customer_report = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                    with gr.Column(scale=1):
                        gr.HTML('<div class="section-title">📊 Auswertung</div>')
                        customer_chart = gr.Plot(label="Kundenkontakte")

                with gr.Row():
                    customer_export_txt_btn = gr.Button("TXT exportieren", elem_classes=["primary-btn"])
                    customer_export_csv_btn = gr.Button("CSV exportieren", elem_classes=["secondary-btn"])
                    customer_export_xlsx_btn = gr.Button("Excel exportieren", elem_classes=["secondary-btn"])
                customer_export_status = gr.Textbox(label="Exportstatus", interactive=False)

        demo.load(
            fn=initial_load,
            outputs=[
                car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
                car_table, car_report, car_chart, car_profit_chart, car_brand_filter, car_edit_select, car_customer, car_id,

                part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
                part_table, part_report, inventory_report, part_chart, part_category_filter, part_edit_select, part_id,

                customer_kpi_1, customer_kpi_2, customer_kpi_3,
                customer_table, customer_report, customer_chart, customer_edit_select, customer_id,
            ],
        )

        login_btn.click(
            fn=login_user,
            inputs=[login_username, login_password],
            outputs=[login_status, login_container, app_container, user_info, user_role],
        )

        logout_btn.click(
            fn=logout_user,
            inputs=[],
            outputs=[login_status, login_container, app_container, user_info, user_role],
        )

        car_brand.blur(fn=smart_capitalize, inputs=[car_brand], outputs=[car_brand])
        car_model.blur(fn=smart_capitalize, inputs=[car_model], outputs=[car_model])
        car_color.blur(fn=smart_capitalize, inputs=[car_color], outputs=[car_color])

        part_name.blur(fn=smart_capitalize, inputs=[part_name], outputs=[part_name])
        part_category.blur(fn=smart_capitalize, inputs=[part_category], outputs=[part_category])
        part_brand.blur(fn=smart_capitalize, inputs=[part_brand], outputs=[part_brand])

        customer_name.blur(fn=smart_capitalize, inputs=[customer_name], outputs=[customer_name])
        customer_address.blur(fn=smart_capitalize, inputs=[customer_address], outputs=[customer_address])

        car_brand.change(fn=suggest_brand_choices, inputs=[car_brand], outputs=[car_brand_suggestions])
        car_brand_suggestions.change(fn=pick_dropdown_value, inputs=[car_brand_suggestions], outputs=[car_brand])

        part_category.change(fn=suggest_category_choices, inputs=[part_category], outputs=[part_category_suggestions])
        part_category_suggestions.change(fn=pick_dropdown_value, inputs=[part_category_suggestions], outputs=[part_category])

        car_add_btn.click(
            fn=add_car,
            inputs=[car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status],
            outputs=[
                car_status_msg, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
                car_chart, car_profit_chart, car_brand_filter, car_edit_select, car_customer, car_id,
                car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
            ],
        )

        car_load_btn.click(
            fn=load_car_for_edit,
            inputs=[car_edit_select],
            outputs=[car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status, car_status_msg],
        )

        car_update_btn.click(
            fn=update_car,
            inputs=[car_edit_select, car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status],
            outputs=[
                car_status_msg, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
                car_chart, car_profit_chart, car_brand_filter, car_edit_select, car_customer, car_id,
                car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
            ],
        )

        car_delete_btn.click(
            fn=delete_car,
            inputs=[car_edit_select],
            outputs=[
                car_status_msg, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
                car_chart, car_profit_chart, car_brand_filter, car_edit_select, car_customer, car_id,
                car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
            ],
        )

        car_clear_btn.click(
            fn=clear_car_form,
            inputs=[],
            outputs=[car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status],
        )

        car_filter_btn.click(
            fn=filter_cars,
            inputs=[car_search, car_brand_filter, car_status_filter],
            outputs=[car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5, car_chart, car_profit_chart],
        )

        car_reset_btn.click(
            fn=reset_cars,
            inputs=[],
            outputs=[car_search, car_brand_filter, car_status_filter, car_table, car_report, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5, car_chart, car_profit_chart],
        )

        car_export_txt_btn.click(fn=export_cars_txt, outputs=[car_export_status])
        car_export_csv_btn.click(fn=export_cars_csv, outputs=[car_export_status])
        car_export_xlsx_btn.click(fn=export_cars_excel, outputs=[car_export_status])

        part_add_btn.click(
            fn=add_part,
            inputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
            outputs=[
                part_status_msg, part_table, part_report, inventory_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
                part_chart, part_category_filter, part_edit_select, part_id,
                part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
            ],
        )

        part_load_btn.click(
            fn=load_part_for_edit,
            inputs=[part_edit_select],
            outputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status, part_status_msg],
        )

        part_update_btn.click(
            fn=update_part,
            inputs=[part_edit_select, part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
            outputs=[
                part_status_msg, part_table, part_report, inventory_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
                part_chart, part_category_filter, part_edit_select, part_id,
                part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
            ],
        )

        part_delete_btn.click(
            fn=delete_part,
            inputs=[part_edit_select],
            outputs=[
                part_status_msg, part_table, part_report, inventory_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
                part_chart, part_category_filter, part_edit_select, part_id,
                part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
            ],
        )

        part_clear_btn.click(
            fn=clear_part_form,
            inputs=[],
            outputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
        )

        part_filter_btn.click(
            fn=filter_parts,
            inputs=[part_search, part_category_filter, part_status_filter],
            outputs=[part_table, part_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4, part_chart, inventory_report],
        )

        part_reset_btn.click(
            fn=reset_parts,
            inputs=[],
            outputs=[part_search, part_category_filter, part_status_filter, part_table, part_report, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4, part_chart, inventory_report],
        )

        part_export_txt_btn.click(fn=export_parts_txt, outputs=[part_export_status])
        part_export_csv_btn.click(fn=export_parts_csv, outputs=[part_export_status])
        part_export_xlsx_btn.click(fn=export_parts_excel, outputs=[part_export_status])

        customer_add_btn.click(
            fn=add_customer,
            inputs=[customer_id, customer_name, customer_phone, customer_email, customer_address],
            outputs=[
                customer_status_msg, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3,
                customer_chart, customer_edit_select, car_customer, customer_id,
                customer_id, customer_name, customer_phone, customer_email, customer_address
            ],
        )

        customer_load_btn.click(
            fn=load_customer_for_edit,
            inputs=[customer_edit_select],
            outputs=[customer_id, customer_name, customer_phone, customer_email, customer_address, customer_status_msg],
        )

        customer_update_btn.click(
            fn=update_customer,
            inputs=[customer_edit_select, customer_id, customer_name, customer_phone, customer_email, customer_address],
            outputs=[
                customer_status_msg, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3,
                customer_chart, customer_edit_select, car_customer, customer_id,
                customer_id, customer_name, customer_phone, customer_email, customer_address
            ],
        )

        customer_delete_btn.click(
            fn=delete_customer,
            inputs=[customer_edit_select],
            outputs=[
                customer_status_msg, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3,
                customer_chart, customer_edit_select, car_customer, customer_id,
                customer_id, customer_name, customer_phone, customer_email, customer_address
            ],
        )

        customer_clear_btn.click(
            fn=clear_customer_form,
            inputs=[],
            outputs=[customer_id, customer_name, customer_phone, customer_email, customer_address],
        )

        customer_filter_btn.click(
            fn=filter_customers,
            inputs=[customer_search],
            outputs=[customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3, customer_chart],
        )

        customer_reset_btn.click(
            fn=reset_customers,
            inputs=[],
            outputs=[customer_search, customer_table, customer_report, customer_kpi_1, customer_kpi_2, customer_kpi_3, customer_chart],
        )

        customer_export_txt_btn.click(fn=export_customers_txt, outputs=[customer_export_status])
        customer_export_csv_btn.click(fn=export_customers_csv, outputs=[customer_export_status])
        customer_export_xlsx_btn.click(fn=export_customers_excel, outputs=[customer_export_status])

    return demo