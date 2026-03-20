from __future__ import annotations
 
import matplotlib.pyplot as plt
 
from src.services.formatting_service import calc_profit, safe_str
 
 
def get_empty_figure(title: str):

    fig, ax = plt.subplots(figsize=(8, 4.0))

    fig.patch.set_facecolor("#071224")

    ax.set_facecolor("#071224")

    ax.text(0.5, 0.5, "Noch keine Daten vorhanden", ha="center", va="center", fontsize=14, color="#cbd5e1")

    ax.set_title(title, color="white", fontsize=14, pad=16)

    ax.axis("off")

    plt.tight_layout()

    return fig
 
 
def get_car_status_chart(data: list[dict] | None = None):

    source = data or []

    counts = {"Verfügbar": 0, "Reserviert": 0, "Verkauft": 0}
 
    for car in source:

        if car["status"] in counts:

            counts[car["status"]] += 1
 
    if sum(counts.values()) == 0:

        return get_empty_figure("Fahrzeuge pro Status")
 
    labels = list(counts.keys())

    values = list(counts.values())
 
    fig, ax = plt.subplots(figsize=(8, 4.0))

    fig.patch.set_facecolor("#071224")

    ax.set_facecolor("#071224")

    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
 
    ax.set_title("Fahrzeuge pro Status", color="white", fontsize=14, pad=16)

    ax.tick_params(axis="x", colors="white")

    ax.tick_params(axis="y", colors="white")

    ax.spines["bottom"].set_color("#64748b")

    ax.spines["left"].set_color("#64748b")

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.25)
 
    for bar, value in zip(bars, values):

        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, str(value), ha="center", va="bottom", color="white")
 
    plt.tight_layout()

    return fig
 
 
def get_part_status_chart(data: list[dict] | None = None):

    source = data or []

    counts = {"Verfügbar": 0, "Nachbestellen": 0, "Nicht verfügbar": 0}
 
    for part in source:

        counts[part["status"]] = counts.get(part["status"], 0) + int(part["stock"])
 
    if sum(counts.values()) == 0:

        return get_empty_figure("Teilebestand nach Status")
 
    labels = list(counts.keys())

    values = list(counts.values())
 
    fig, ax = plt.subplots(figsize=(8, 4.0))

    fig.patch.set_facecolor("#071224")

    ax.set_facecolor("#071224")

    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
 
    ax.set_title("Teilebestand nach Status", color="white", fontsize=14, pad=16)

    ax.tick_params(axis="x", colors="white")

    ax.tick_params(axis="y", colors="white")

    ax.spines["bottom"].set_color("#64748b")

    ax.spines["left"].set_color("#64748b")

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.25)
 
    for bar, value in zip(bars, values):

        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, str(value), ha="center", va="bottom", color="white")
 
    plt.tight_layout()

    return fig
 
 
def get_customer_chart(data: list[dict] | None = None):

    source = data or []

    if not source:

        return get_empty_figure("Kundenkontakte")
 
    labels = ["Mit E-Mail", "Mit Telefon", "Ohne Kontakt"]

    with_email = sum(1 for c in source if safe_str(c["email"]))

    with_phone = sum(1 for c in source if safe_str(c["phone"]))

    without_contact = sum(1 for c in source if not safe_str(c["email"]) and not safe_str(c["phone"]))

    values = [with_email, with_phone, without_contact]
 
    fig, ax = plt.subplots(figsize=(8, 4.0))

    fig.patch.set_facecolor("#071224")

    ax.set_facecolor("#071224")

    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
 
    ax.set_title("Kundenkontakte", color="white", fontsize=14, pad=16)

    ax.tick_params(axis="x", colors="white")

    ax.tick_params(axis="y", colors="white")

    ax.spines["bottom"].set_color("#64748b")

    ax.spines["left"].set_color("#64748b")

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.25)
 
    for bar, value in zip(bars, values):

        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, str(value), ha="center", va="bottom", color="white")
 
    plt.tight_layout()

    return fig
 
 
def get_profit_trend_chart(data: list[dict] | None = None):

    source = data or []

    sold_cars = [car for car in source if safe_str(car.get("status")) == "Verkauft"]
 
    if not sold_cars:

        return get_empty_figure("Gewinn pro verkauftem Fahrzeug")
 
    labels = [f"{car['brand']} {car['model']}" for car in sold_cars]

    values = [calc_profit(car["purchase_price"], car["sale_price"]) for car in sold_cars]
 
    fig, ax = plt.subplots(figsize=(10, 4.5))

    fig.patch.set_facecolor("#071224")

    ax.set_facecolor("#071224")

    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
 
    ax.set_title("Gewinn pro verkauftem Fahrzeug", color="white", fontsize=14, pad=16)

    ax.tick_params(axis="x", colors="white", rotation=25)

    ax.tick_params(axis="y", colors="white")

    ax.spines["bottom"].set_color("#64748b")

    ax.spines["left"].set_color("#64748b")

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.25)
 
    for bar, value in zip(bars, values):

        ax.text(

            bar.get_x() + bar.get_width() / 2,

            value + 0.03,

            f"{value:.0f}",

            ha="center",

            va="bottom",

            color="white",

            fontsize=9,

        )
 
    plt.tight_layout()

    return fig
 