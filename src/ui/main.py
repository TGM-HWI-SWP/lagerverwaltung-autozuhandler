from __future__ import annotations

import gradio as gr

from src.domain.enums import CAR_STATUSES, PART_STATUSES, INVOICE_STATUSES, FUELS
from src.services.auth_service import authenticate
from src.services.formatting_service import smart_capitalize
from src.app_context import (
    car_service,
    part_service,
    customer_service,
    filter_service,
    dashboard_service,
    export_service,
    car_report,
    part_report,
    customer_report,
    next_car_id,
    next_part_id,
    next_customer_id,
    get_customer_name_by_id,
)
from src.ui.ui_helpers import (
    suggest_brand_choices,
    suggest_category_choices,
    pick_dropdown_value,
    get_customer_choices,
    extract_customer_id,
    get_brand_choices,
    get_category_choices,
    get_car_id_choices,
    get_part_id_choices,
    get_customer_id_choices,
    clear_car_form,
    clear_part_form,
    clear_customer_form,
    refresh_car_view,
    refresh_part_view,
    refresh_customer_view,
    initial_load,
)
from src.ui.charts import get_car_chart, get_part_chart, get_customer_chart


APP_TITLE = "Autozuhändler"

custom_css = """
:root {
    --bg: #030712;
    --panel: #071224;
    --panel-2: #0b1730;
    --panel-3: #0f1d3b;
    --border: rgba(148, 163, 184, 0.18);
    --text: #f8fafc;
    --muted: #cbd5e1;
}

.gradio-container {
    background: linear-gradient(135deg, #020617 0%, #071224 45%, #0b1020 100%) !important;
    color: var(--text) !important;
}

#dashboard-root, #dashboard-root * {
    box-sizing: border-box;
}

#dashboard-root .gr-block, #dashboard-root .block {
    border-radius: 20px !important;
    border: 1px solid var(--border) !important;
    background: rgba(7, 18, 36, 0.92) !important;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.28) !important;
}

#dashboard-root .gr-row, #dashboard-root .gr-column, #dashboard-root .gr-group, #dashboard-root .gr-box {
    overflow: visible !important;
}

#dashboard-root h1, #dashboard-root h2, #dashboard-root h3, #dashboard-root h4, #dashboard-root p, #dashboard-root label {
    color: var(--text) !important;
}

.main-title {
    padding: 8px 4px 18px 4px;
}

.main-title h1 {
    font-size: 36px !important;
    font-weight: 800 !important;
    margin-bottom: 6px !important;
}

.main-title p {
    color: var(--muted) !important;
    margin: 0 !important;
    font-size: 15px !important;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
}

.subtle-text {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 10px;
}

.kpi-card {
    display: flex;
    align-items: center;
    gap: 14px;
    min-height: 92px;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: linear-gradient(145deg, rgba(10,18,35,0.96), rgba(16,29,58,0.92));
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.26);
}

.kpi-card.blue { border-color: rgba(56, 189, 248, 0.20); }
.kpi-card.green { border-color: rgba(34, 197, 94, 0.20); }
.kpi-card.violet { border-color: rgba(139, 92, 246, 0.20); }
.kpi-card.gold { border-color: rgba(245, 158, 11, 0.20); }

.kpi-icon {
    min-width: 52px;
    height: 52px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.06);
    font-size: 24px;
}

.kpi-body {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.kpi-title {
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}

.kpi-value {
    color: var(--text);
    font-size: 18px;
    font-weight: 800;
    line-height: 1.2;
    word-break: break-word;
}

#dashboard-root input, #dashboard-root textarea {
    background: rgba(15, 23, 42, 0.92) !important;
    color: #ffffff !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    border-radius: 14px !important;
}

#dashboard-root input:focus, #dashboard-root textarea:focus {
    border-color: rgba(56, 189, 248, 0.65) !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.16) !important;
}

#dashboard-root .primary-btn button,
#dashboard-root .secondary-btn button,
#dashboard-root .danger-btn button {
    border-radius: 14px !important;
    font-weight: 700 !important;
    transition: all 0.18s ease !important;
}

#dashboard-root .primary-btn button:hover,
#dashboard-root .secondary-btn button:hover,
#dashboard-root .danger-btn button:hover {
    transform: translateY(-1px);
}

#dashboard-root [role="listbox"], #dashboard-root .options, #dashboard-root .wrap, #dashboard-root .dropdown, #dashboard-root .menu {
    z-index: 9999 !important;
}

#dashboard-root .gr-dataframe {
    border-radius: 18px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: rgba(7, 18, 36, 0.95) !important;
}

#dashboard-root table {
    border-radius: 18px !important;
    overflow: hidden !important;
}

#dashboard-root thead tr th {
    background: rgba(15, 29, 59, 0.96) !important;
    color: #f8fafc !important;
    font-weight: 700 !important;
    border-bottom: 1px solid rgba(148,163,184,0.16) !important;
}

#dashboard-root tbody tr {
    background: rgba(7, 18, 36, 0.88) !important;
}

#dashboard-root tbody tr:nth-child(even) {
    background: rgba(10, 20, 40, 0.95) !important;
}

#dashboard-root tbody td {
    color: #e2e8f0 !important;
    border-bottom: 1px solid rgba(148,163,184,0.08) !important;
}

.report-box textarea {
    font-family: Consolas, monospace !important;
    line-height: 1.45 !important;
}

.legend-box {
    padding: 12px 14px;
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(148, 163, 184, 0.18);
    color: #e2e8f0;
}

footer {
    display: none !important;
}
"""


def login_user(username, password):
    ok, message, name, role = authenticate(username, password)
    if not ok:
        return message, gr.update(visible=True), gr.update(visible=False), "", ""
    return message, gr.update(visible=False), gr.update(visible=True), name, role


def logout_user():
    return "Abgemeldet.", gr.update(visible=True), gr.update(visible=False), "", ""


def add_car_handler(
    car_id, brand, model, year, mileage, fuel, color,
    purchase_price, sale_price, customer_choice, invoice_status, status
):
    try:
        customer_id = extract_customer_id(customer_choice)
        car = car_service.add_car(
            car_id, brand, model, year, mileage, fuel, color,
            purchase_price, sale_price, customer_id, invoice_status, status
        )
        return (
            *refresh_car_view(status_message=f"Fahrzeug '{car.brand} {car.model}' wurde gespeichert."),
            *clear_car_form()
        )
    except ValueError as e:
        return (
            *refresh_car_view(status_message=str(e)),
            car_id, brand, model, fuel, year, mileage, color,
            purchase_price, sale_price, customer_choice, invoice_status, status
        )


def load_car_for_edit(selected_id):
    if not selected_id:
        return "", "", "", None, "", "", "", "", "", "-", "Offen", None, "Bitte zuerst ein Fahrzeug auswählen."

    car = car_service.get_car(selected_id)
    if not car:
        return "", "", "", None, "", "", "", "", "", "-", "Offen", None, "Fahrzeug nicht gefunden."

    customer_value = "-"
    if car.customer_id:
        customer_value = f"{car.customer_id} | {get_customer_name_by_id(car.customer_id)}"

    return (
        car.id,
        car.brand,
        car.model,
        car.fuel,
        str(car.year),
        str(car.mileage),
        car.color,
        str(car.purchase_price),
        str(car.sale_price),
        customer_value,
        car.invoice_status,
        car.status,
        f"Fahrzeug '{selected_id}' geladen."
    )


def update_car_handler(
    selected_id, car_id, brand, model, fuel, year, mileage, color,
    purchase_price, sale_price, customer_choice, invoice_status, status
):
    try:
        customer_id = extract_customer_id(customer_choice)
        car = car_service.update_car(
            selected_id, brand, model, fuel, year, mileage, color,
            purchase_price, sale_price, customer_id, invoice_status, status
        )

        customer_value = "-"
        if car.customer_id:
            customer_value = f"{car.customer_id} | {get_customer_name_by_id(car.customer_id)}"

        return (
            *refresh_car_view(status_message=f"Fahrzeug '{selected_id}' wurde aktualisiert."),
            car.id,
            car.brand,
            car.model,
            car.fuel,
            str(car.year),
            str(car.mileage),
            car.color,
            str(car.purchase_price),
            str(car.sale_price),
            customer_value,
            car.invoice_status,
            car.status
        )
    except ValueError as e:
        return (
            *refresh_car_view(status_message=str(e)),
            car_id, brand, model, fuel, year, mileage, color,
            purchase_price, sale_price, customer_choice, invoice_status, status
        )


def delete_car_handler(selected_id):
    try:
        car = car_service.delete_car(selected_id)
        return (
            *refresh_car_view(status_message=f"Fahrzeug '{selected_id}' ({car.brand} {car.model}) wurde gelöscht."),
            *clear_car_form()
        )
    except ValueError as e:
        return (
            *refresh_car_view(status_message=str(e)),
            *clear_car_form()
        )


def filter_cars_handler(search_term, brand_filter, status_filter):
    data = filter_service.filter_cars(search_term, brand_filter, status_filter)
    return (
        dashboard_service.cars_to_dataframe(data),
        car_report.build_text(data) if data else "Keine passenden Fahrzeuge gefunden.",
        *dashboard_service.get_car_dashboard_cards(data),
        get_car_chart(data),
    )


def add_part_handler(part_id, name, category, brand, price, stock, status):
    try:
        part = part_service.add_part(part_id, name, category, brand, price, stock, status)
        return (
            *refresh_part_view(status_message=f"Teil '{part.name}' wurde gespeichert."),
            *clear_part_form()
        )
    except ValueError as e:
        return (
            *refresh_part_view(status_message=str(e)),
            part_id, name, category, brand, price, stock, status
        )


def load_part_for_edit(selected_id):
    if not selected_id:
        return "", "", "", "", "", "", None, "Bitte zuerst ein Teil auswählen."

    part = part_service.get_part(selected_id)
    if not part:
        return "", "", "", "", "", "", None, "Teil nicht gefunden."

    return (
        part.id,
        part.name,
        part.category,
        part.brand,
        str(part.price),
        str(part.stock),
        part.status,
        f"Teil '{selected_id}' geladen."
    )


def update_part_handler(selected_id, part_id, name, category, brand, price, stock, status):
    try:
        part = part_service.update_part(selected_id, name, category, brand, price, stock, status)
        return (
            *refresh_part_view(status_message=f"Teil '{selected_id}' wurde aktualisiert."),
            part.id, part.name, part.category, part.brand, str(part.price), str(part.stock), part.status
        )
    except ValueError as e:
        return (
            *refresh_part_view(status_message=str(e)),
            part_id, name, category, brand, price, stock, status
        )


def delete_part_handler(selected_id):
    try:
        part = part_service.delete_part(selected_id)
        return (
            *refresh_part_view(status_message=f"Teil '{selected_id}' ({part.name}) wurde gelöscht."),
            *clear_part_form()
        )
    except ValueError as e:
        return (
            *refresh_part_view(status_message=str(e)),
            *clear_part_form()
        )


def filter_parts_handler(search_term, category_filter, status_filter):
    data = filter_service.filter_parts(search_term, category_filter, status_filter)
    return (
        dashboard_service.parts_to_dataframe(data),
        part_report.build_text(data) if data else "Keine passenden Teile gefunden.",
        *dashboard_service.get_part_dashboard_cards(data),
        get_part_chart(data),
    )


def add_customer_handler(customer_id, name, phone, email, address):
    try:
        customer = customer_service.add_customer(customer_id, name, phone, email, address)
        return (
            *refresh_customer_view(status_message=f"Kunde '{customer.name}' wurde gespeichert."),
            *clear_customer_form()
        )
    except ValueError as e:
        return (
            *refresh_customer_view(status_message=str(e)),
            customer_id, name, phone, email, address
        )


def load_customer_for_edit(selected_id):
    if not selected_id:
        return "", "", "", "", "", "Bitte zuerst einen Kunden auswählen."

    customer = customer_service.get_customer(selected_id)
    if not customer:
        return "", "", "", "", "", "Kunde nicht gefunden."

    return (
        customer.id,
        customer.name,
        customer.phone,
        customer.email,
        customer.address,
        f"Kunde '{selected_id}' geladen."
    )


def update_customer_handler(selected_id, customer_id, name, phone, email, address):
    try:
        customer = customer_service.update_customer(selected_id, name, phone, email, address)
        return (
            *refresh_customer_view(status_message=f"Kunde '{selected_id}' wurde aktualisiert."),
            customer.id, customer.name, customer.phone, customer.email, customer.address
        )
    except ValueError as e:
        return (
            *refresh_customer_view(status_message=str(e)),
            customer_id, name, phone, email, address
        )


def delete_customer_handler(selected_id):
    try:
        customer = customer_service.delete_customer(selected_id)
        return (
            *refresh_customer_view(status_message=f"Kunde '{selected_id}' ({customer.name}) wurde gelöscht."),
            *clear_customer_form()
        )
    except ValueError as e:
        return (
            *refresh_customer_view(status_message=str(e)),
            *clear_customer_form()
        )


def filter_customers_handler(search_term):
    data = filter_service.filter_customers(search_term)
    return (
        dashboard_service.customers_to_dataframe(data),
        customer_report.build_text(data) if data else "Keine passenden Kunden gefunden.",
        *dashboard_service.get_customer_dashboard_cards(data),
        get_customer_chart(data),
    )


def export_cars_txt():
    return export_service.export_text_report(
        "fahrzeugreport",
        car_report.build_text(car_service.list_all())
    )


def export_parts_txt():
    return export_service.export_text_report(
        "teile_report",
        part_report.build_text(part_service.list_all())
    )


def export_customers_txt():
    return export_service.export_text_report(
        "kunden_report",
        customer_report.build_text(customer_service.list_all())
    )


def export_cars_csv():
    return export_service.export_dataframe_csv(
        dashboard_service.cars_to_dataframe(car_service.list_all()),
        "fahrzeuge"
    )


def export_parts_csv():
    return export_service.export_dataframe_csv(
        dashboard_service.parts_to_dataframe(part_service.list_all()),
        "teile"
    )


def export_customers_csv():
    return export_service.export_dataframe_csv(
        dashboard_service.customers_to_dataframe(customer_service.list_all()),
        "kunden"
    )


def export_cars_excel():
    return export_service.export_dataframe_excel(
        dashboard_service.cars_to_dataframe(car_service.list_all()),
        "fahrzeuge"
    )


def export_parts_excel():
    return export_service.export_dataframe_excel(
        dashboard_service.parts_to_dataframe(part_service.list_all()),
        "teile"
    )


def export_customers_excel():
    return export_service.export_dataframe_excel(
        dashboard_service.customers_to_dataframe(customer_service.list_all()),
        "kunden"
    )


with gr.Blocks(title=APP_TITLE, elem_id="dashboard-root") as demo:
    current_user_name = gr.State("")
    current_user_role = gr.State("")

    login_container = gr.Column(visible=True)
    app_container = gr.Column(visible=False)

    with login_container:
        gr.HTML("""
        <div class="main-title">
            <h1>Autozuhändler</h1>
            <p>Mitarbeiter-Login für Fahrzeuge, Teile, Kunden und Verkaufsverwaltung.</p>
        </div>
        """)
        with gr.Row():
            with gr.Column(scale=1):
                login_username = gr.Textbox(label="Benutzername")
                login_password = gr.Textbox(label="Passwort", type="password")
                login_btn = gr.Button("Anmelden", variant="primary", elem_classes=["primary-btn"])
                login_status = gr.Textbox(label="Status", interactive=False)
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="legend-box">
                    <b>Demo-Zugänge</b><br><br>
                    Julian / admin123<br>
                    Fabienne / admin456<br>
                    Mikail / admin789<br>
                    Sirin / admin000<br>
                    lehrer / lehrer123
                </div>
                """)

    with app_container:
        gr.HTML("""
        <div class="main-title">
            <h1>Autozuhändler</h1>
            <p>Verwaltung von Fahrzeugen, Teilen, Kunden, Verkauf, Rechnungsstatus und Exporten.</p>
        </div>
        """)

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
                    gr.HTML('<div class="section-title">🚘 Fahrzeug anlegen / bearbeiten</div><div class="subtle-text">Automatische ID, Ankauf, Verkauf, Gewinn, Kunde und Rechnungsstatus.</div>')

                    car_edit_select = gr.Dropdown(label="Fahrzeug wählen", choices=[], value=None)
                    with gr.Row():
                        car_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                        car_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                    car_id = gr.Textbox(label="Fahrzeug-ID", interactive=False, value=next_car_id())
                    car_brand = gr.Textbox(label="Marke")
                    car_brand_suggestions = gr.Dropdown(label="Marken-Vorschläge", choices=[], value=None)
                    car_model = gr.Textbox(label="Modell")
                    car_year = gr.Textbox(label="Baujahr")
                    car_mileage = gr.Textbox(label="Kilometerstand")
                    car_fuel = gr.Dropdown(choices=FUELS, label="Kraftstoff", value=None)
                    car_color = gr.Textbox(label="Farbe")
                    car_purchase_price = gr.Textbox(label="Ankaufspreis")
                    car_sale_price = gr.Textbox(label="Verkaufspreis")
                    car_customer = gr.Dropdown(label="Kunde", choices=get_customer_choices(), value="-")
                    car_invoice_status = gr.Dropdown(choices=INVOICE_STATUSES, label="Rechnungsstatus", value="Offen")
                    car_status = gr.Dropdown(choices=CAR_STATUSES, label="Status", value=None)

                    with gr.Row():
                        car_add_btn = gr.Button("Neues Fahrzeug speichern", variant="primary", elem_classes=["primary-btn"])
                        car_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                        car_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                    car_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                with gr.Column(scale=2):
                    gr.HTML('<div class="section-title">📋 Fahrzeugbestand</div><div class="subtle-text">Suche nach ID, Marke, Kunde, Status und Verkaufsstand.</div>')
                    car_table = gr.Dataframe(interactive=False, label="Fahrzeugbestand")

            with gr.Row():
                car_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Marke, Modell, Kunde, Status")
                car_brand_filter = gr.Dropdown(label="🏷️ Marke filtern", choices=["Alle"] + get_brand_choices(), value="Alle", filterable=True)
                car_status_filter = gr.Dropdown(label="📌 Status filtern", choices=["Alle"] + CAR_STATUSES, value="Alle")

            with gr.Row():
                car_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                car_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">🧾 Fahrzeugreport</div>')
                    car_report_box = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">📊 Auswertung</div>')
                    car_chart = gr.Plot(label="Fahrzeuge pro Status")

            with gr.Row():
                car_export_txt_btn = gr.Button("TXT exportieren in Nextcloud", variant="primary", elem_classes=["primary-btn"])
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
                    gr.HTML('<div class="section-title">📦 Teil anlegen / bearbeiten</div><div class="subtle-text">Mit Ampel-Status für Lagerverfügbarkeit.</div>')

                    part_edit_select = gr.Dropdown(label="Teil wählen", choices=[], value=None)
                    with gr.Row():
                        part_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                        part_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                    part_id = gr.Textbox(label="Teile-ID", interactive=False, value=next_part_id())
                    part_name = gr.Textbox(label="Teilename")
                    part_category = gr.Textbox(label="Kategorie")
                    part_category_suggestions = gr.Dropdown(label="Kategorie-Vorschläge", choices=[], value=None)
                    part_brand = gr.Textbox(label="Marke / Hersteller")
                    part_price = gr.Textbox(label="Preis")
                    part_stock = gr.Textbox(label="Bestand")
                    part_status = gr.Dropdown(choices=PART_STATUSES, label="Lagerstatus", value=None)

                    gr.HTML("""
                    <div class="legend-box">
                        <b>Ampelstatus</b><br>
                        🟢 Verfügbar<br>
                        🟡 Nachbestellen<br>
                        🔴 Nicht verfügbar
                    </div>
                    """)

                    with gr.Row():
                        part_add_btn = gr.Button("Neues Teil speichern", variant="primary", elem_classes=["primary-btn"])
                        part_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                        part_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                    part_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                with gr.Column(scale=2):
                    gr.HTML('<div class="section-title">🗂️ Teilelager</div><div class="subtle-text">Lagerwert, Bestand und Ampelstatus.</div>')
                    part_table = gr.Dataframe(interactive=False, label="Teilebestand")

            with gr.Row():
                part_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Name, Kategorie, Marke, Status")
                part_category_filter = gr.Dropdown(label="🏷️ Kategorie filtern", choices=["Alle"] + get_category_choices(), value="Alle", filterable=True)
                part_status_filter = gr.Dropdown(label="📌 Status filtern", choices=["Alle"] + PART_STATUSES, value="Alle")

            with gr.Row():
                part_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                part_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">🧾 Teile-Report</div>')
                    part_report_box = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">📊 Auswertung</div>')
                    part_chart = gr.Plot(label="Teilebestand nach Status")

            with gr.Row():
                part_export_txt_btn = gr.Button("TXT exportieren in Nextcloud", variant="primary", elem_classes=["primary-btn"])
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
                    gr.HTML('<div class="section-title">👤 Kunde anlegen / bearbeiten</div><div class="subtle-text">Automatische Kunden-ID und Zuordnung zu Verkäufen.</div>')

                    customer_edit_select = gr.Dropdown(label="Kunde wählen", choices=[], value=None)
                    with gr.Row():
                        customer_load_btn = gr.Button("Laden", elem_classes=["secondary-btn"])
                        customer_delete_btn = gr.Button("Löschen", elem_classes=["danger-btn"])

                    customer_id = gr.Textbox(label="Kunden-ID", interactive=False, value=next_customer_id())
                    customer_name = gr.Textbox(label="Name")
                    customer_phone = gr.Textbox(label="Telefon")
                    customer_email = gr.Textbox(label="E-Mail")
                    customer_address = gr.Textbox(label="Adresse", lines=3)

                    with gr.Row():
                        customer_add_btn = gr.Button("Neuen Kunden speichern", variant="primary", elem_classes=["primary-btn"])
                        customer_update_btn = gr.Button("Änderungen speichern", elem_classes=["secondary-btn"])
                        customer_clear_btn = gr.Button("Formular leeren", elem_classes=["secondary-btn"])

                    customer_status_msg = gr.Textbox(label="Statusmeldung", interactive=False)

                with gr.Column(scale=2):
                    gr.HTML('<div class="section-title">👥 Kundenverwaltung</div><div class="subtle-text">Alle Kunden mit Kontaktübersicht.</div>')
                    customer_table = gr.Dataframe(interactive=False, label="Kunden")

            with gr.Row():
                customer_search = gr.Textbox(label="🔎 Suche", placeholder="ID, Name, Telefon, E-Mail, Adresse")
                customer_filter_btn = gr.Button("Filter anwenden", elem_classes=["secondary-btn"])
                customer_reset_btn = gr.Button("Ansicht zurücksetzen", elem_classes=["secondary-btn"])

            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">🧾 Kundenreport</div>')
                    customer_report_box = gr.Textbox(label="Report", lines=18, interactive=False, elem_classes=["report-box"])
                with gr.Column(scale=1):
                    gr.HTML('<div class="section-title">📊 Auswertung</div>')
                    customer_chart = gr.Plot(label="Kundenkontakte")

            with gr.Row():
                customer_export_txt_btn = gr.Button("TXT exportieren in Nextcloud", variant="primary", elem_classes=["primary-btn"])
                customer_export_csv_btn = gr.Button("CSV exportieren", elem_classes=["secondary-btn"])
                customer_export_xlsx_btn = gr.Button("Excel exportieren", elem_classes=["secondary-btn"])
            customer_export_status = gr.Textbox(label="Exportstatus", interactive=False)

    demo.load(
        fn=initial_load,
        outputs=[
            car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_table, car_report_box, car_chart, car_brand_filter, car_edit_select, car_customer, car_id,

            part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_table, part_report_box, part_chart, part_category_filter, part_edit_select, part_id,

            customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_table, customer_report_box, customer_chart, customer_edit_select, customer_id,
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
        fn=add_car_handler,
        inputs=[
            car_id, car_brand, car_model, car_year, car_mileage, car_fuel, car_color,
            car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
        outputs=[
            car_status_msg, car_table, car_report_box, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_chart, car_brand_filter, car_edit_select, car_customer, car_id,
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
    )

    car_load_btn.click(
        fn=load_car_for_edit,
        inputs=[car_edit_select],
        outputs=[
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage, car_color,
            car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status, car_status_msg
        ],
    )

    car_update_btn.click(
        fn=update_car_handler,
        inputs=[
            car_edit_select, car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
        outputs=[
            car_status_msg, car_table, car_report_box, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_chart, car_brand_filter, car_edit_select, car_customer, car_id,
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
    )

    car_delete_btn.click(
        fn=delete_car_handler,
        inputs=[car_edit_select],
        outputs=[
            car_status_msg, car_table, car_report_box, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_chart, car_brand_filter, car_edit_select, car_customer, car_id,
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
    )

    car_clear_btn.click(
        fn=clear_car_form,
        outputs=[
            car_id, car_brand, car_model, car_fuel, car_year, car_mileage,
            car_color, car_purchase_price, car_sale_price, car_customer, car_invoice_status, car_status
        ],
    )

    car_filter_btn.click(
        fn=filter_cars_handler,
        inputs=[car_search, car_brand_filter, car_status_filter],
        outputs=[car_table, car_report_box, car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5, car_chart],
    )

    car_reset_btn.click(
        fn=lambda: (
            "",
            "Alle",
            "Alle",
            dashboard_service.cars_to_dataframe(car_service.list_all()),
            car_report.build_text(car_service.list_all()),
            *dashboard_service.get_car_dashboard_cards(car_service.list_all()),
            get_car_chart(car_service.list_all())
        ),
        inputs=[],
        outputs=[
            car_search, car_brand_filter, car_status_filter,
            car_table, car_report_box,
            car_kpi_1, car_kpi_2, car_kpi_3, car_kpi_4, car_kpi_5,
            car_chart
        ],
    )

    car_export_txt_btn.click(fn=export_cars_txt, outputs=[car_export_status])
    car_export_csv_btn.click(fn=export_cars_csv, outputs=[car_export_status])
    car_export_xlsx_btn.click(fn=export_cars_excel, outputs=[car_export_status])

    part_add_btn.click(
        fn=add_part_handler,
        inputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
        outputs=[
            part_status_msg, part_table, part_report_box, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
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
        fn=update_part_handler,
        inputs=[part_edit_select, part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
        outputs=[
            part_status_msg, part_table, part_report_box, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_chart, part_category_filter, part_edit_select, part_id,
            part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
        ],
    )

    part_delete_btn.click(
        fn=delete_part_handler,
        inputs=[part_edit_select],
        outputs=[
            part_status_msg, part_table, part_report_box, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_chart, part_category_filter, part_edit_select, part_id,
            part_id, part_name, part_category, part_brand, part_price, part_stock, part_status
        ],
    )

    part_clear_btn.click(
        fn=clear_part_form,
        outputs=[part_id, part_name, part_category, part_brand, part_price, part_stock, part_status],
    )

    part_filter_btn.click(
        fn=filter_parts_handler,
        inputs=[part_search, part_category_filter, part_status_filter],
        outputs=[part_table, part_report_box, part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4, part_chart],
    )

    part_reset_btn.click(
        fn=lambda: (
            "",
            "Alle",
            "Alle",
            dashboard_service.parts_to_dataframe(part_service.list_all()),
            part_report.build_text(part_service.list_all()),
            *dashboard_service.get_part_dashboard_cards(part_service.list_all()),
            get_part_chart(part_service.list_all())
        ),
        inputs=[],
        outputs=[
            part_search, part_category_filter, part_status_filter,
            part_table, part_report_box,
            part_kpi_1, part_kpi_2, part_kpi_3, part_kpi_4,
            part_chart
        ],
    )

    part_export_txt_btn.click(fn=export_parts_txt, outputs=[part_export_status])
    part_export_csv_btn.click(fn=export_parts_csv, outputs=[part_export_status])
    part_export_xlsx_btn.click(fn=export_parts_excel, outputs=[part_export_status])

    customer_add_btn.click(
        fn=add_customer_handler,
        inputs=[customer_id, customer_name, customer_phone, customer_email, customer_address],
        outputs=[
            customer_status_msg, customer_table, customer_report_box, customer_kpi_1, customer_kpi_2, customer_kpi_3,
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
        fn=update_customer_handler,
        inputs=[customer_edit_select, customer_id, customer_name, customer_phone, customer_email, customer_address],
        outputs=[
            customer_status_msg, customer_table, customer_report_box, customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_chart, customer_edit_select, car_customer, customer_id,
            customer_id, customer_name, customer_phone, customer_email, customer_address
        ],
    )

    customer_delete_btn.click(
        fn=delete_customer_handler,
        inputs=[customer_edit_select],
        outputs=[
            customer_status_msg, customer_table, customer_report_box, customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_chart, customer_edit_select, car_customer, customer_id,
            customer_id, customer_name, customer_phone, customer_email, customer_address
        ],
    )

    customer_clear_btn.click(
        fn=clear_customer_form,
        outputs=[customer_id, customer_name, customer_phone, customer_email, customer_address],
    )

    customer_filter_btn.click(
        fn=filter_customers_handler,
        inputs=[customer_search],
        outputs=[customer_table, customer_report_box, customer_kpi_1, customer_kpi_2, customer_kpi_3, customer_chart],
    )

    customer_reset_btn.click(
        fn=lambda: (
            "",
            dashboard_service.customers_to_dataframe(customer_service.list_all()),
            customer_report.build_text(customer_service.list_all()),
            *dashboard_service.get_customer_dashboard_cards(customer_service.list_all()),
            get_customer_chart(customer_service.list_all())
        ),
        inputs=[],
        outputs=[
            customer_search,
            customer_table, customer_report_box,
            customer_kpi_1, customer_kpi_2, customer_kpi_3,
            customer_chart
        ],
    )

    customer_export_txt_btn.click(fn=export_customers_txt, outputs=[customer_export_status])
    customer_export_csv_btn.click(fn=export_customers_csv, outputs=[customer_export_status])
    customer_export_xlsx_btn.click(fn=export_customers_excel, outputs=[customer_export_status])


if __name__ == "_main_":
    demo.launch(
        theme=gr.themes.Base(),
        css=custom_css,
    )