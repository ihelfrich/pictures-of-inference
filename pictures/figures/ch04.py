"""
Figures for Chapter 4: The grammar of graphics.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_SINGLE, FIG_FULL, FIG_SPREAD,
)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


@poi_style(size=(8.5, 5.5))
def fig_grammar():
    """Anatomy of a chart: data, aesthetics, geometry, exploded."""
    fig, axes = plt.subplots(1, 3, figsize=(9, 4.5))

    # Panel 1: tabular data
    ax = axes[0]
    rng = np.random.default_rng(42)
    x = rng.uniform(0, 10, 8)
    y = 0.6 * x + rng.normal(0, 1, 8)
    cats = rng.choice(["A", "B"], 8)
    ax.axis("off")
    ax.set_title("1. Data\n(rectangle)", fontsize=10, pad=10)
    ax.text(0.5, 0.95, "x      y      cat", ha="center",
            family="monospace", fontsize=9, transform=ax.transAxes,
            color=DIM, fontweight="bold")
    for i in range(8):
        ax.text(0.5, 0.85 - i * 0.09,
                f"{x[i]:5.2f} {y[i]:5.2f}   {cats[i]}",
                ha="center", family="monospace", fontsize=9,
                transform=ax.transAxes, color=INK)

    # Panel 2: aesthetic mapping (text annotation)
    ax = axes[1]
    ax.axis("off")
    ax.set_title("2. Aesthetic mappings", fontsize=10, pad=10)
    mappings = [
        ("x", "→  position-x", INK),
        ("y", "→  position-y", INK),
        ("cat", "→  color", RUST),
    ]
    for i, (col, target, color) in enumerate(mappings):
        ax.text(0.5, 0.7 - i * 0.18, f"{col} {target}",
                ha="center", fontsize=11, transform=ax.transAxes,
                color=color, family="monospace")

    # Panel 3: rendered chart
    ax = axes[2]
    colors = [INK if c == "A" else RUST for c in cats]
    ax.scatter(x, y, c=colors, s=70, edgecolor="white", linewidth=1.2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("3. Geometry: point", fontsize=10, pad=10)
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=(9, 5.5))
def fig_perceptual_hierarchy():
    """Same five values rendered five ways."""
    values = np.array([18, 27, 12, 31, 22])
    labels = list("ABCDE")
    colors = [INK, RUST, SAGE, GOLD, VIOLET]

    fig, axes = plt.subplots(1, 5, figsize=(11, 4))
    titles = [
        "Position\n(common axis)",
        "Length\n(bars)",
        "Angle\n(pie)",
        "Area\n(circles)",
        "Color\n(saturation)",
    ]

    # 1. Position on common axis (dot plot)
    ax = axes[0]
    ax.scatter(values, range(len(labels)), s=80, color=INK, zorder=3)
    for i, v in enumerate(values):
        ax.plot([0, v], [i, i], color=DIM, alpha=0.3, zorder=1)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xlim(0, 35)
    ax.set_title(titles[0], fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 2. Length (bars)
    ax = axes[1]
    ax.barh(range(len(labels)), values, color=INK, edgecolor="white")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_title(titles[1], fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 3. Angle (pie)
    ax = axes[2]
    ax.pie(values, labels=labels, colors=colors,
           startangle=90, wedgeprops=dict(edgecolor="white"))
    ax.set_title(titles[2], fontsize=10)

    # 4. Area (circles)
    ax = axes[3]
    sizes = np.sqrt(values) * 30  # area scales with values, radius with sqrt
    for i, (v, label) in enumerate(zip(values, labels)):
        ax.scatter([i], [0.5], s=v * 90, color=INK, alpha=0.6,
                   edgecolor=INK)
        ax.text(i, 0.05, label, ha="center", fontsize=11, color=INK)
    ax.set_xlim(-0.7, len(labels) - 0.3)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(titles[3], fontsize=10)
    for s in ax.spines.values():
        s.set_visible(False)

    # 5. Color saturation
    ax = axes[4]
    norm = (values - values.min()) / (values.max() - values.min())
    for i, (v, label) in enumerate(zip(norm, labels)):
        ax.add_patch(
            plt.Rectangle((i - 0.4, 0), 0.8, 1,
                          facecolor=plt.cm.Blues(0.3 + 0.6 * v),
                          edgecolor="white"))
        ax.text(i, -0.12, label, ha="center", fontsize=11, color=INK)
    ax.set_xlim(-0.7, len(labels) - 0.3)
    ax.set_ylim(-0.2, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(titles[4], fontsize=10)
    for s in ax.spines.values():
        s.set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=(8.5, 5.5))
def fig_faceting():
    """Faceted scatter: y vs x by group."""
    rng = np.random.default_rng(7)
    countries = ["USA", "CHN", "DEU", "JPN", "GBR", "KOR"]
    fig, axes = plt.subplots(2, 3, figsize=(9, 5), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, country in enumerate(countries):
        ax = axes[i]
        n = 40
        x = rng.uniform(0.5, 25, n)
        slope = 0.3 + 0.1 * i
        y = slope * x ** 0.7 * np.exp(rng.normal(0, 0.4, n))
        ax.scatter(np.log(x), np.log(y), s=22, color=INK, alpha=0.7,
                   edgecolor="white", linewidth=0.4)
        ax.set_title(country, fontsize=9)
        ax.set_xlim(-1, 4)
        ax.set_ylim(-2, 3)
        ax.grid(True, alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if i in (3, 4, 5):
            ax.set_xlabel("log(importer GDP)")
        if i in (0, 3):
            ax.set_ylabel("log(exports)")

    plt.tight_layout()
    return fig


@poi_style(size=(8.5, 4))
def fig_palette():
    """Show the seven semantic colors with labels."""
    fig, ax = plt.subplots()
    palette = [
        ("INK", INK, "primary, default, the main story"),
        ("RUST", RUST, "treatment, contrast, alternative"),
        ("SAGE", SAGE, "control, comparison, baseline"),
        ("GOLD", GOLD, "highlighted, derived"),
        ("VIOLET", VIOLET, "uncertain, predicted"),
        ("DIM", DIM, "background, de-emphasized"),
        ("TEAL", TEAL, "secondary contrast"),
    ]

    for i, (name, color, desc) in enumerate(palette):
        y = len(palette) - i - 0.5
        ax.add_patch(plt.Rectangle((0, y - 0.4), 1.0, 0.8,
                                   facecolor=color, edgecolor="white",
                                   linewidth=2))
        ax.text(0.5, y, name, ha="center", va="center",
                color="white", fontweight="bold", fontsize=11)
        ax.text(1.2, y, desc, ha="left", va="center",
                fontsize=10, color=INK)

    ax.set_xlim(-0.05, 5.5)
    ax.set_ylim(-0.2, len(palette) + 0.2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    return fig


@poi_style(size=(9, 6))
def fig_same_data_four_ways():
    """One small dataset, four geometries: scatter, bar, dot plot, slope."""
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.5))

    # Synthetic small dataset: 5 countries, 2 years' worth of values
    countries = ["USA", "CHN", "DEU", "JPN", "GBR"]
    v_2014 = np.array([18.5, 10.5, 3.8, 4.9, 2.9])
    v_2023 = np.array([27.4, 17.8, 4.5, 4.2, 3.3])

    # 1. Scatter (2014 vs 2023)
    ax = axes[0, 0]
    ax.scatter(v_2014, v_2023, s=80, color=INK, edgecolor="white", linewidth=1.2)
    for i, c in enumerate(countries):
        ax.annotate(c, (v_2014[i], v_2023[i]),
                    xytext=(5, 5), textcoords="offset points", fontsize=9,
                    color=INK)
    lo, hi = 0, 30
    ax.plot([lo, hi], [lo, hi], color=DIM, linestyle="dashed",
            linewidth=0.8, label="y = x")
    ax.set_xlabel("GDP 2014 (USD T)")
    ax.set_ylabel("GDP 2023 (USD T)")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_title("Scatter — relationship", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 2. Bar (2023 ranked)
    ax = axes[0, 1]
    order = np.argsort(v_2023)
    ax.barh([countries[i] for i in order], v_2023[order], color=INK,
            edgecolor="white")
    ax.set_xlabel("GDP 2023 (USD T)")
    ax.set_title("Bar — ranking", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 3. Dot plot
    ax = axes[1, 0]
    for i in order:
        ax.plot([0, v_2023[i]], [i, i], color=DIM, alpha=0.4)
    ax.scatter(v_2023[order], range(len(countries)),
               s=80, color=INK, zorder=3)
    ax.set_yticks(range(len(countries)))
    ax.set_yticklabels([countries[i] for i in order])
    ax.set_xlabel("GDP 2023 (USD T)")
    ax.set_title("Dot plot — ranking, less ink", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 4. Slope graph
    ax = axes[1, 1]
    for i, c in enumerate(countries):
        color = INK if v_2023[i] - v_2014[i] > 0 else RUST
        ax.plot([0, 1], [v_2014[i], v_2023[i]], "o-",
                color=color, linewidth=1.6, markersize=6)
        ax.text(-0.04, v_2014[i], c, ha="right", va="center",
                fontsize=9, color=INK)
        ax.text(1.04, v_2023[i], c, ha="left", va="center",
                fontsize=9, color=color)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["2014", "2023"])
    ax.set_xlim(-0.25, 1.25)
    ax.set_title("Slope graph — change over time", fontsize=10)
    ax.set_ylabel("GDP (USD T)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig
