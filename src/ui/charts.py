import gradio as gr
 
from src.domain.enums import DEFAULT_BRANDS, DEFAULT_CATEGORIES

from src.services.formatting_service import normalize_db_list, safe_str

from src.app_context import (

    car_service, part_service, customer_service,

    dashboard_service, car_report, part_report, customer_report,

    next_car_id, next_part_id, next_customer_id, get_customer_name_by_id

)

from src.ui.charts import get_car_chart, get_part_chart, get_customer_chart
 
 
def get_brand_choices():

    values = DEFAULT_BRANDS + [car.brand for car in car_service.list_all() if car.brand]

    return normalize_db_list(values)
 
 
def get_category_choices():

    values = DEFAULT_CATEGORIES + [part.category for part in part_service.list_all() if part.category]

    return normalize_db_list(values)
 
 
def make_choice_suggestions(search_text, source_list):

    text = safe_str(search_text).lower()

    if not text:

        result = source_list[:8]

    else:

        starts = [v for v in source_list if v.lower().startswith(text)]

        contains = [v for v in source_list if text in v.lower() and v not in starts]

        result = (starts + contains)[:8]

    return gr.update(choices=result, value=None)
 
 
def suggest_brand_choices(search_text):

    return make_choice_suggestions(search_text, get_brand_choices())
 
 
def suggest_category_choices(search_text):

    return make_choice_suggestions(search_text, get_category_choices())
 
 
def pick_dropdown_value(value):

    return value or ""
 
 
def get_customer_choices(include_empty: bool = True):

    choices = []

    if include_empty:

        choices.append("-")

    for customer in customer_service.list_all():

        choices.append(f"{customer.id} | {customer.name}")

    return choices
 
 
def extract_customer_id(choice: str) -> str:

    value = safe_str(choice)

    if not value or value == "-":

        return ""

    return value.split("|")[0].strip()
 
 
def get_car_id_choices():

    return [car.id for car in car_service.list_all()]
 
 
def get_part_id_choices():

    return [part.id for part in part_service.list_all()]
 
 
def get_customer_id_choices():

    return [customer.id for customer in customer_service.list_all()]
 
 
def clear_car_form():

    return (

        next_car_id(),

        "",

        "",

        None,

        "",

        "",

        "",

        "",

        "",

        "-",

        "Offen",

        None,

    )
 
 
def clear_part_form():

    return next_part_id(), "", "", "", "", "", None
 
 
def clear_customer_form():

    return next_customer_id(), "", "", "", ""
 
 
def refresh_car_view(filtered_data=None, status_message=""):

    data = filtered_data if filtered_data is not None else car_service.list_all()

    report_text = car_report.build_text(data) if data else "Keine passenden Fahrzeuge gefunden."

    return (

        status_message,

        dashboard_service.cars_to_dataframe(data),

        report_text,

        *dashboard_service.get_car_dashboard_cards(data),

        get_car_chart(data),

        gr.update(choices=["Alle"] + get_brand_choices(), value="Alle"),

        gr.update(choices=get_car_id_choices(), value=None),

        gr.update(choices=get_customer_choices(), value="-"),

        next_car_id(),

    )
 
 
def refresh_part_view(filtered_data=None, status_message=""):

    data = filtered_data if filtered_data is not None else part_service.list_all()

    report_text = part_report.build_text(data) if data else "Keine passenden Teile gefunden."

    return (

        status_message,

        dashboard_service.parts_to_dataframe(data),

        report_text,

        *dashboard_service.get_part_dashboard_cards(data),

        get_part_chart(data),

        gr.update(choices=["Alle"] + get_category_choices(), value="Alle"),

        gr.update(choices=get_part_id_choices(), value=None),

        next_part_id(),

    )
 
 
def refresh_customer_view(filtered_data=None, status_message=""):

    data = filtered_data if filtered_data is not None else customer_service.list_all()

    report_text = customer_report.build_text(data) if data else "Keine passenden Kunden gefunden."

    return (

        status_message,

        dashboard_service.customers_to_dataframe(data),

        report_text,

        *dashboard_service.get_customer_dashboard_cards(data),

        get_customer_chart(data),

        gr.update(choices=get_customer_id_choices(), value=None),

        gr.update(choices=get_customer_choices(), value="-"),

        next_customer_id(),

    )
 
 
def initial_load():

    car_data = car_service.list_all()

    part_data = part_service.list_all()

    customer_data = customer_service.list_all()
 
    return (

        *dashboard_service.get_car_dashboard_cards(car_data),

        dashboard_service.cars_to_dataframe(car_data),

        car_report.build_text(car_data),

        get_car_chart(car_data),

        gr.update(choices=["Alle"] + get_brand_choices(), value="Alle"),

        gr.update(choices=get_car_id_choices(), value=None),

        gr.update(choices=get_customer_choices(), value="-"),

        next_car_id(),
 
        *dashboard_service.get_part_dashboard_cards(part_data),

        dashboard_service.parts_to_dataframe(part_data),

        part_report.build_text(part_data),

        get_part_chart(part_data),

        gr.update(choices=["Alle"] + get_category_choices(), value="Alle"),

        gr.update(choices=get_part_id_choices(), value=None),

        next_part_id(),
 
        *dashboard_service.get_customer_dashboard_cards(customer_data),

        dashboard_service.customers_to_dataframe(customer_data),

        customer_report.build_text(customer_data),

        get_customer_chart(customer_data),

        gr.update(choices=get_customer_id_choices(), value=None),

        next_customer_id(),

    )
 