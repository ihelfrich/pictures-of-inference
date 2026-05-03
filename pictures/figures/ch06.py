"""
Figures for Chapter 6: Lying with charts.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_FULL, FIG_SPREAD,
)
import matplotlib.pyplot as plt
import numpy as np


@poi_style(size=(8.5, 4))
def fig_truncated_axis():
    """Same data, full y-axis vs truncated."""
    labels = ["A", "B"]
    values = [100, 102]

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))

    # Honest
    ax = axes[0]
    ax.bar(labels, values, color=INK, edgecolor="white", width=0.55)
    ax.set_ylim(0, 110)
    ax.set_title("Honest: y-axis starts at 0", fontsize=10)
    ax.set_ylabel("value")
    for i, v in enumerate(values):
        ax.text(i, v + 2, str(v), ha="center", color=INK, fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Lying
    ax = axes[1]
    ax.bar(labels, values, color=RUST, edgecolor="white", width=0.55)
    ax.set_ylim(99, 103)
    ax.set_title("Misleading: y-axis truncated to [99, 103]", fontsize=10)
    for i, v in enumerate(values):
        ax.text(i, v + 0.05, str(v), ha="center", color=RUST, fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=(8.5, 4))
def fig_cherry_pick():
    """Full series vs cherry-picked window."""
    rng = np.random.default_rng(7)
    years = np.arange(1994, 2024)
    trend = 30 + 1.2 * (years - 1994)
    noise = rng.normal(0, 4, len(years))
    series = trend + noise

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))

    ax = axes[0]
    ax.plot(years, series, "o-", color=INK, markersize=4, linewidth=1.2)
    ax.set_title("Full series, 1994-2023:  upward trend", fontsize=10)
    ax.set_xlabel("year")
    ax.set_ylabel("value")
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Picked window: years 2007-2012 where the noise creates a downward stretch
    pick_lo, pick_hi = 2007, 2012
    mask = (years >= pick_lo) & (years <= pick_hi)
    ax = axes[1]
    ax.plot(years[mask], series[mask], "o-", color=RUST,
            markersize=5, linewidth=1.2)
    ax.set_xlim(pick_lo - 0.5, pick_hi + 0.5)
    ax.set_title(f"Window {pick_lo}-{pick_hi}:  apparent decline",
                 fontsize=10)
    ax.set_xlabel("year")
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=(8.5, 4.5))
def fig_area_distortion():
    """Same 2x ratio, encoded as length vs as area."""
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4.5))

    # Honest: bars only differ in height
    ax = axes[0]
    ax.bar([0, 1], [100, 200], width=0.6, color=INK,
           edgecolor="white")
    ax.text(0, 105, "100", ha="center", color=INK, fontsize=11)
    ax.text(1, 205, "200", ha="center", color=INK, fontsize=11)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["A", "B"])
    ax.set_ylim(0, 240)
    ax.set_title("Honest: 2× height for 2× value", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Misleading: bar B is also 2x wider
    ax = axes[1]
    ax.add_patch(plt.Rectangle((-0.25, 0), 0.5, 100,
                               facecolor=RUST, edgecolor="white"))
    ax.add_patch(plt.Rectangle((0.5, 0), 1.0, 200,
                               facecolor=RUST, edgecolor="white"))
    ax.text(0, 105, "100", ha="center", color=RUST, fontsize=11)
    ax.text(1, 205, "200", ha="center", color=RUST, fontsize=11)
    ax.text(0.5, -25,
            "B's area is 4× A's area,\nbut the value is only 2×",
            ha="center", color=RUST, fontsize=9, style="italic")
    ax.set_xlim(-0.7, 1.7)
    ax.set_ylim(-50, 240)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["A", "B"])
    ax.set_title("Misleading: bar widened too", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=FIG_FULL)
def fig_dual_axis():
    """Two unrelated series rigged to look correlated by axis manipulation."""
    rng = np.random.default_rng(2026)
    t = np.arange(0, 50)
    series1 = 30 + 8 * np.sin(t / 6) + rng.normal(0, 1.0, len(t))   # range ~22-38
    series2 = 6 + 0.5 * np.sin(t / 6 + 0.4) + rng.normal(0, 0.05, len(t))  # range ~5.5-6.5

    fig, ax1 = plt.subplots()
    ax1.plot(t, series1, color=INK, linewidth=1.5, label="series 1 (left)")
    ax1.set_ylabel("series 1", color=INK)
    ax1.tick_params(axis="y", labelcolor=INK)
    ax1.set_xlabel("time")
    ax1.set_ylim(0, 50)
    ax1.spines["top"].set_visible(False)

    ax2 = ax1.twinx()
    ax2.plot(t, series2, color=RUST, linewidth=1.5, label="series 2 (right)")
    ax2.set_ylabel("series 2", color=RUST)
    ax2.tick_params(axis="y", labelcolor=RUST)
    ax2.set_ylim(5, 7)
    ax2.spines["top"].set_visible(False)

    ax1.set_title("Two unrelated series, rigged dual axes", fontsize=11)
    return fig


@poi_style(size=(8.5, 4))
def fig_log_hides():
    """Same exponential data on linear vs log axis."""
    t = np.arange(0, 25)
    y = 2 ** t  # explosive growth

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))

    ax = axes[0]
    ax.plot(t, y, "o-", color=INK, linewidth=1.5)
    ax.set_title("Linear axis:  exponential growth screams", fontsize=10)
    ax.set_xlabel("time")
    ax.set_ylabel("value")
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    ax.plot(t, y, "o-", color=RUST, linewidth=1.5)
    ax.set_yscale("log")
    ax.set_title("Log axis:  the same growth looks gentle", fontsize=10)
    ax.set_xlabel("time")
    ax.set_ylabel("value (log)")
    ax.grid(True, which="both", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig
