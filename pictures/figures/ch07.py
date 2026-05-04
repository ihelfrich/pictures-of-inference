"""
Figures for Chapter 7: Underused visualizations.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_FULL, FIG_SPREAD,
)
from poi.data import trade as load_trade
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np


@poi_style(size=(8, 6))
def fig_slope_graph():
    """Slope graph: each country's exports to USA in 2014 vs 2023."""
    rows = load_trade()
    # exports to USA from each non-USA country, 2014 vs 2023
    exporters = ["CHN", "DEU", "JPN", "GBR", "KOR"]
    v_2014 = {}
    v_2023 = {}
    for r in rows:
        if r["importer"] == "USA" and r["exporter"] in exporters:
            if r["year"] == 2014:
                v_2014[r["exporter"]] = r["exports_usd_millions"] / 1000
            elif r["year"] == 2023:
                v_2023[r["exporter"]] = r["exports_usd_millions"] / 1000

    fig, ax = plt.subplots()
    for c in exporters:
        a, b = v_2014[c], v_2023[c]
        color = INK if b >= a else RUST
        ax.plot([0, 1], [a, b], "o-", color=color, linewidth=1.8,
                markersize=7)
        ax.text(-0.04, a, f"{c}  {a:.1f}", ha="right", va="center",
                fontsize=10, color=INK)
        ax.text(1.04, b, f"{b:.1f}  {c}", ha="left", va="center",
                fontsize=10, color=color)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["2014", "2023"], fontsize=11)
    ax.set_xlim(-0.30, 1.30)
    ax.set_ylabel("Exports to USA (USD billions)")
    ax.set_title("Slope graph: bilateral exports to the United States",
                 fontsize=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_dot_plot():
    """Cleveland dot plot: total exports by country in 2023."""
    rows = load_trade()
    countries = ["USA", "CHN", "DEU", "JPN", "GBR", "KOR"]
    totals = {c: 0.0 for c in countries}
    for r in rows:
        if r["year"] == 2023:
            totals[r["exporter"]] += r["exports_usd_millions"] / 1000

    order = sorted(totals.items(), key=lambda x: x[1])
    labels = [k for k, _ in order]
    values = [v for _, v in order]

    fig, ax = plt.subplots()
    for i, (lab, val) in enumerate(zip(labels, values)):
        ax.plot([0, val], [i, i], color=DIM, alpha=0.5, linewidth=0.8)
        ax.scatter([val], [i], s=110, color=INK, zorder=3,
                   edgecolor="white", linewidth=1.5)
        ax.text(val + max(values) * 0.012, i, f"{val:.0f}",
                ha="left", va="center", fontsize=10, color=INK)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Total exports in 2023 (USD billions)")
    ax.set_xlim(0, max(values) * 1.18)
    ax.set_title("Cleveland dot plot: total exports, ranked",
                 fontsize=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=(9, 6))
def fig_hex_bin():
    """Hex bin of 100k slightly correlated noisy points."""
    rng = np.random.default_rng(42)
    n = 100_000
    # Build a slightly tilted joint distribution with two modes
    z1 = rng.normal(0, 1, n)
    z2 = rng.normal(0, 1, n)
    x = z1 + 0.4 * z2 + rng.normal(0, 0.5, n)
    y = 0.5 * z1 - 0.3 * z2 + rng.normal(0, 0.5, n)
    # Add a small second blob
    mask = rng.random(n) < 0.15
    x[mask] += 2.5
    y[mask] += 1.5

    fig, ax = plt.subplots()
    hb = ax.hexbin(x, y, gridsize=45, mincnt=1, cmap="Blues")
    cb = fig.colorbar(hb, ax=ax, label="point count")
    ax.set_xlabel("variable 1")
    ax.set_ylabel("variable 2")
    ax.set_title(f"Hex bin: 100,000 points, two visible modes",
                 fontsize=12)
    ax.grid(False)
    return fig


@poi_style(size=(8, 7))
def fig_ridge_plot():
    """Ridge plot: distribution of log exports across years."""
    rows = load_trade()
    by_year = {}
    for r in rows:
        by_year.setdefault(r["year"], []).append(
            np.log(r["exports_usd_millions"]))
    years = sorted(by_year.keys())

    fig, ax = plt.subplots()
    n_years = len(years)
    spacing = 0.9
    grid = np.linspace(2, 14, 400)

    for i, y in enumerate(years):
        vals = np.array(by_year[y])
        # KDE by hand: gaussian kernel
        h = 0.5
        density = sum(np.exp(-((grid - v) / h) ** 2 / 2) /
                      (h * np.sqrt(2 * np.pi)) for v in vals) / len(vals)
        density = density / density.max() * 0.85  # normalize per row
        offset = (n_years - 1 - i) * spacing
        # Color from INK to TEAL gradient
        t = i / max(1, n_years - 1)
        color = (
            (1 - t) * np.array([0.10, 0.31, 0.48]) +
            t * np.array([0.23, 0.54, 0.60])
        )
        ax.fill_between(grid, offset, offset + density,
                        color=color, alpha=0.75, edgecolor="white",
                        linewidth=0.8)
        ax.plot(grid, offset + density, color="white", linewidth=0.8)
        ax.text(grid[0] - 0.3, offset + 0.3, str(y),
                ha="right", va="center", fontsize=10, color=INK)

    ax.set_xlim(grid[0] - 1.0, grid[-1])
    ax.set_ylim(-0.3, n_years * spacing + 0.5)
    ax.set_xlabel("log(exports) USD millions")
    ax.set_yticks([])
    ax.set_title("Ridge plot: distribution of log bilateral exports across years",
                 fontsize=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    return fig


@poi_style(size=(8.5, 5.5))
def fig_mosaic():
    """Mosaic plot: simulated survival by class."""
    rng = np.random.default_rng(7)
    # Simulated: First class better survival than second, second better than third
    counts = {
        ("1st", "survived"): 200,
        ("1st", "perished"): 122,
        ("2nd", "survived"): 119,
        ("2nd", "perished"): 167,
        ("3rd", "survived"): 181,
        ("3rd", "perished"): 528,
    }
    classes = ["1st", "2nd", "3rd"]
    outcomes = ["survived", "perished"]
    total = sum(counts.values())
    class_totals = {c: counts[(c, "survived")] + counts[(c, "perished")]
                    for c in classes}

    fig, ax = plt.subplots()
    color_for = {"survived": SAGE, "perished": RUST}

    x = 0
    gap = 0.012
    for ci, c in enumerate(classes):
        w = class_totals[c] / total
        y = 0
        for oi, o in enumerate(outcomes):
            h = counts[(c, o)] / class_totals[c]
            ax.add_patch(Rectangle(
                (x, y), w - gap, h - gap,
                facecolor=color_for[o], alpha=0.85,
                edgecolor="white", linewidth=1.5))
            # Label inside if room
            if w * h > 0.04:
                ax.text(x + w / 2, y + h / 2,
                        f"{counts[(c, o)]}",
                        ha="center", va="center",
                        color="white", fontsize=10, fontweight="bold")
            y += h
        # Class label below
        ax.text(x + w / 2, -0.06, c, ha="center", va="center",
                fontsize=11, color=INK, fontweight="bold")
        x += w

    # Outcome legend
    handles = [mpatches.Patch(facecolor=color_for[o], label=o, alpha=0.85)
               for o in outcomes]
    ax.legend(handles=handles, loc="upper center",
              bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.10, 1.02)
    ax.set_aspect("auto")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Mosaic plot: survival by passenger class (simulated)",
                 fontsize=12)
    for s in ax.spines.values():
        s.set_visible(False)
    return fig


@poi_style(size=(9, 6))
def fig_alluvial():
    """Simple alluvial: rank changes 2014 -> 2023 for partner countries."""
    rows = load_trade()
    countries = ["CHN", "DEU", "JPN", "GBR", "KOR"]

    # Each country's total exports to USA in each year
    exp_2014 = {c: 0 for c in countries}
    exp_2023 = {c: 0 for c in countries}
    for r in rows:
        if r["importer"] == "USA" and r["exporter"] in countries:
            if r["year"] == 2014:
                exp_2014[r["exporter"]] = r["exports_usd_millions"]
            elif r["year"] == 2023:
                exp_2023[r["exporter"]] = r["exports_usd_millions"]

    rank_2014 = sorted(countries, key=lambda c: -exp_2014[c])
    rank_2023 = sorted(countries, key=lambda c: -exp_2023[c])

    n = len(countries)
    fig, ax = plt.subplots()
    band_h = 0.85 / n

    color_map = {c: clr for c, clr in
                 zip(countries, [INK, RUST, SAGE, GOLD, VIOLET])}

    for c in countries:
        i = rank_2014.index(c)
        j = rank_2023.index(c)
        y0 = 0.95 - i * (1.0 / n) - band_h / 2
        y1 = 0.95 - j * (1.0 / n) - band_h / 2
        # Bezier-ish curve via parametric cubic
        ts = np.linspace(0, 1, 100)
        xs = ts
        # Smooth s-curve
        s = 3 * ts ** 2 - 2 * ts ** 3
        ys_top = (1 - s) * (y0 + band_h / 2) + s * (y1 + band_h / 2)
        ys_bot = (1 - s) * (y0 - band_h / 2) + s * (y1 - band_h / 2)
        ax.fill_between(xs, ys_bot, ys_top,
                        color=color_map[c], alpha=0.55,
                        edgecolor=color_map[c], linewidth=0.4)
        # Endpoint labels
        ax.text(-0.03, y0, c, ha="right", va="center",
                fontsize=11, color=color_map[c], fontweight="bold")
        ax.text(1.03, y1, c, ha="left", va="center",
                fontsize=11, color=color_map[c], fontweight="bold")

    # Header labels
    ax.text(0.0, 1.04, "2014 rank", ha="left", va="bottom",
            fontsize=10, color=INK, fontweight="bold")
    ax.text(1.0, 1.04, "2023 rank", ha="right", va="bottom",
            fontsize=10, color=INK, fontweight="bold")

    ax.set_xlim(-0.16, 1.16)
    ax.set_ylim(-0.05, 1.10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Alluvial: rank as US importer, 2014 to 2023",
                 fontsize=12)
    for s in ax.spines.values():
        s.set_visible(False)
    return fig
