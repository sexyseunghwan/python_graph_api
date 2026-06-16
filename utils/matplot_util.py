import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import numpy as np
from decimal import Decimal
from typing import BinaryIO

from models.consume import ConsumeInfo


def visualize_consume_res_by_category(
    category_labels: list[str],
    category_size_labels: list[float],
    start_dt: str,
    end_date: str,
    total_cost: float,
    image_buffer: BinaryIO,
) -> None:
    _draw_circle_graph(category_size_labels, category_labels, False, 140, start_dt, end_date, total_cost, image_buffer)


def _draw_circle_graph(
    category_size_labels: list[float],
    category_labels: list[str],
    shadow: bool,
    startangle: int,
    start_dt: str,
    end_date: str,
    total_cost: float,
    image_buffer: BinaryIO,
) -> None:
    colors = plt.cm.viridis(np.linspace(0, 1, len(category_size_labels)))

    plt.figure(figsize=(8, 8))
    plt.pie(category_size_labels, labels=category_labels, colors=colors,
            autopct='%1.1f%%', shadow=shadow, startangle=startangle)
    plt.axis('equal')
    plt.suptitle(f"[{start_dt} ~ {end_date}]", fontsize=16)
    plt.title(f"Total Cost: {int(total_cost):,}", fontsize=10, color='black', loc='center', pad=20)
    plt.savefig(image_buffer, format='png')
    plt.close()


def draw_asset_pie_graph(
    category_labels: list[str],
    category_amounts_krw: list[float],
    total_asset_amount_krw: Decimal,
    image_buffer: BinaryIO,
) -> None:
    colors = plt.cm.viridis(np.linspace(0, 1, len(category_amounts_krw)))
    labels = [
        f"{label}\n{int(amount):,}"
        for label, amount in zip(category_labels, category_amounts_krw)
    ]

    plt.figure(figsize=(8, 8))
    plt.pie(
        category_amounts_krw,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140,
    )
    plt.axis('equal')
    plt.suptitle("Asset Category Ratio", fontsize=16)
    plt.title(
        f"Total Asset: {int(total_asset_amount_krw):,} KRW",
        fontsize=10,
        color='black',
        loc='center',
        pad=20,
    )
    plt.savefig(image_buffer, format='png')
    plt.close()


def _thousands_formatter(x: float, pos: int) -> str:
    return f'{int(x):,}'


def _apply_line_graph_style(title: str, x_label: str, y_label: str, image_buffer: BinaryIO) -> None:
    formatter = FuncFormatter(_thousands_formatter)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig(image_buffer, format='png')
    plt.close()


def draw_line_graph_dual(
    consume_info_1: ConsumeInfo,
    consume_info_2: ConsumeInfo,
    image_buffer: BinaryIO,
) -> None:
    # Work on copies to avoid mutating the input objects.
    list_1 = list(consume_info_1.consume_res_list)
    list_2 = list(consume_info_2.consume_res_list)

    if not list_1 and not list_2:
        list_1.append(0)
        list_2.append(0)
    elif len(list_1) != len(list_2):
        shorter, longer = (list_1, list_2) if len(list_1) < len(list_2) else (list_2, list_1)
        last = shorter[-1] if shorter else 0
        shorter.extend([last] * (len(longer) - len(shorter)))

    longer_len = max(len(list_1), len(list_2), 1)
    x = list(range(1, longer_len + 1))

    if longer_len == 1:
        list_1.append(list_1[-1])
        list_2.append(list_2[-1])
        x.append(2)

    plt.figure(figsize=(10, 7))
    plt.plot(x, list_1, color='red', label=f"[{consume_info_1.start_date} ~ {consume_info_1.end_date}]")
    plt.plot(x, list_2, color='black', label=f"[{consume_info_2.start_date} ~ {consume_info_2.end_date}]")

    _apply_line_graph_style(
        f"[{consume_info_1.start_date} ~ {consume_info_1.end_date}] {int(consume_info_1.total_cost):,} won",
        'Date', 'Consume Cost', image_buffer,
    )


def draw_line_graph_single(consume_info: ConsumeInfo, image_buffer: BinaryIO) -> None:
    x = list(range(1, len(consume_info.consume_res_list) + 1))

    plt.figure(figsize=(10, 7))
    plt.plot(x, consume_info.consume_res_list, color='red',
             label=f"[{consume_info.start_date} ~ {consume_info.end_date}]")

    _apply_line_graph_style(
        f"[{consume_info.start_date} ~ {consume_info.end_date}] {int(consume_info.total_cost):,} won",
        'Date', 'Consume Cost', image_buffer,
    )
