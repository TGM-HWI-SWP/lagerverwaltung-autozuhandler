from __future__ import annotations

import matplotlib.pyplot as plt

from domain.enums import CarStatus, PartStatus
from domain.models.car import Car
from domain.models.customer import Customer
from domain.models.part import Part


def get_empty_figure(title: str):
    fig, ax = plt.subplots(figsize=(8, 4.0))
    fig.patch.set_facecolor("#071224")
    ax.set_facecolor("#071224")
    ax.text(
        0.5,
        0.5,
        "Noch keine Daten vorhanden",
        ha="center",
        va="center",
        fontsize=14,
        color="#cbd5e1",
    )
    ax.set_title(title, color="white", fontsize=14, pad=16)
    ax.axis("off")
    plt.tight_layout()
    return fig


def _style_axes(ax, title: str) -> None:
    ax.set_title(title, color="white", fontsize=14, pad=16)
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.spines["bottom"].set_color("#64748b")
    ax.spines["left"].set_color("#64748b")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.25)


def _apply_dark_background(fig, ax) -> None:
    fig.patch.set_facecolor("#071224")
    ax.set_facecolor("#071224")


def _annotate_bars(ax, bars, values: list[int]) -> None:
    offset = 0.03 if max(values, default=0) <= 5 else max(values) * 0.01
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            str(value),
            ha="center",
            va="bottom",
            color="white",
        )


def get_car_chart(cars: list[Car]):
    counts = {
        CarStatus.AVAILABLE.value: 0,
        CarStatus.RESERVED.value: 0,
        CarStatus.SOLD.value: 0,
    }

    for car in cars:
        counts[car.status.value] = counts.get(car.status.value, 0) + 1

    if sum(counts.values()) == 0:
        return get_empty_figure("Fahrzeuge pro Status")

    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(8, 4.0))
    _apply_dark_background(fig, ax)
    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
    _style_axes(ax, "Fahrzeuge pro Status")
    _annotate_bars(ax, bars, values)
    plt.tight_layout()
    return fig


def get_part_chart(parts: list[Part]):
    counts = {
        PartStatus.AVAILABLE.value: 0,
        PartStatus.REORDER.value: 0,
        PartStatus.UNAVAILABLE.value: 0,
    }

    for part in parts:
        counts[part.status.value] = counts.get(part.status.value, 0) + part.stock

    if sum(counts.values()) == 0:
        return get_empty_figure("Teilebestand nach Status")

    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(8, 4.0))
    _apply_dark_background(fig, ax)
    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
    _style_axes(ax, "Teilebestand nach Status")
    _annotate_bars(ax, bars, values)
    plt.tight_layout()
    return fig


def get_customer_chart(customers: list[Customer]):
    if not customers:
        return get_empty_figure("Kundenkontakte")

    labels = ["Mit E-Mail", "Mit Telefon", "Ohne Kontakt"]
    with_email = sum(1 for c in customers if c.email.strip())
    with_phone = sum(1 for c in customers if c.phone.strip())
    without_contact = sum(1 for c in customers if not c.email.strip() and not c.phone.strip())
    values = [with_email, with_phone, without_contact]

    fig, ax = plt.subplots(figsize=(8, 4.0))
    _apply_dark_background(fig, ax)
    bars = ax.bar(labels, values, edgecolor="white", linewidth=1)
    _style_axes(ax, "Kundenkontakte")
    _annotate_bars(ax, bars, values)
    plt.tight_layout()
    return fig