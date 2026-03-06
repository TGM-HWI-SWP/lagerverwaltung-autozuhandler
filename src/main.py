import gradio as gr


# Dummy-Daten
products = []


def add_product(product_id, name, description, price, quantity):
    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        return "Preis muss eine Zahl sein und Menge eine ganze Zahl.", get_product_list(), get_report()

    product = {
        "id": product_id,
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
    }

    products.append(product)

    return (
        f"Produkt '{name}' wurde hinzugefügt.",
        get_product_list(),
        get_report(),
    )


def get_product_list():
    if not products:
        return "Noch keine Produkte vorhanden."

    text = ""
    for p in products:
        text += (
            f"ID: {p['id']} | "
            f"Name: {p['name']} | "
            f"Beschreibung: {p['description']} | "
            f"Preis: {p['price']} € | "
            f"Menge: {p['quantity']}\n"
        )
    return text


def get_report():
    if not products:
        return "Kein Report möglich, da keine Produkte vorhanden sind."

    total_products = len(products)
    total_quantity = sum(p["quantity"] for p in products)
    total_value = sum(p["price"] * p["quantity"] for p in products)

    report = (
        "Autozuhändler Lager Report\n"
        "---------------------------\n"
        f"Anzahl Produkte: {total_products}\n"
        f"Gesamtmenge: {total_quantity}\n"
        f"Gesamtwert Lager: {total_value:.2f} €\n"
    )
    return report


with gr.Blocks(title="Autozuhändler System") as demo:
    gr.Markdown("# Autozuhändler System")
    gr.Markdown("Dummy-Oberfläche für Produkte, Liste und Lager-Report")

    with gr.Row():
        with gr.Column():
            product_id = gr.Textbox(label="Produkt-ID")
            name = gr.Textbox(label="Name")
            description = gr.Textbox(label="Beschreibung")
            price = gr.Textbox(label="Preis")
            quantity = gr.Textbox(label="Menge")

            add_button = gr.Button("Produkt hinzufügen")

            status_output = gr.Textbox(label="Status", interactive=False)

        with gr.Column():
            product_list_output = gr.Textbox(
                label="Produkte im Lager",
                lines=12,
                interactive=False,
            )

            report_output = gr.Textbox(
                label="Lager Report",
                lines=8,
                interactive=False,
            )

    add_button.click(
        fn=add_product,
        inputs=[product_id, name, description, price, quantity],
        outputs=[status_output, product_list_output, report_output],
    )


if __name__ == "__main__":
    demo.launch()