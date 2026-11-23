"""Построение четырёх графиков по titanic.csv. Запуск: python3 plot_titanic.py."""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator, MultipleLocator

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "plots"
CLASSES = [1, 2, 3]
COLORS = ["#42758B", "#BF7840", "#51836C"]


def make_axes(title, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    ax.set(title=title, xlabel="Класс билета", ylabel=ylabel, xlim=(0.5, 3.5))
    ax.set_xticks(CLASSES)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax


def save(fig, filename):
    fig.savefig(OUTPUT / filename, dpi=300)
    plt.close(fig)


def counts_plot(counts, title, filename, maximum):
    fig, ax = make_axes(title, "Число пассажиров, чел.")
    bars = ax.bar(CLASSES, counts, color=COLORS, width=0.58)
    ax.bar_label(bars, padding=5)
    ax.set_ylim(0, maximum * 1.15)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    save(fig, filename)


def main():
    try:
        font_manager.findfont("Times New Roman", fallback_to_default=False)
    except ValueError as error:
        raise SystemExit("Для построения графиков установите шрифт Times New Roman.") from error
    plt.rcParams.update({"font.family": "Times New Roman", "font.size": 15,
                         "axes.titlesize": 21, "axes.titlepad": 14})
    data = pd.read_csv(ROOT / "titanic.csv")
    OUTPUT.mkdir(exist_ok=True)
    counts = pd.crosstab(data["Pclass"], data["Sex"]).reindex(
        index=CLASSES, columns=["male", "female"], fill_value=0)
    maximum = counts.to_numpy().max()
    counts_plot(counts["male"], "Распределение мужчин по классам", "men.png", maximum)
    counts_plot(counts["female"], "Распределение женщин по классам", "women.png", maximum)

    fig, ax = make_axes("Возраст пассажиров по классам", "Возраст, лет")
    ages = [data.loc[data["Pclass"] == cls, "Age"].dropna() for cls in CLASSES]
    boxes = ax.boxplot(ages, positions=CLASSES, widths=0.48, patch_artist=True,
                       medianprops={"color": "black", "linewidth": 2})
    for box, color in zip(boxes["boxes"], COLORS):
        box.set_facecolor(color)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    save(fig, "age.png")

    survivors = data.loc[data["Survived"] == 1, "Pclass"].value_counts().reindex(CLASSES, fill_value=0)
    counts_plot(survivors, "Число выживших пассажиров по классам", "survivors.png", survivors.max())


if __name__ == "__main__":
    main()
