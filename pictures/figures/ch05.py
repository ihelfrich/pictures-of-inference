"""
Figures for Chapter 5: Center, spread, shape.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_FULL, FIG_SPREAD,
)
import matplotlib.pyplot as plt
import numpy as np


def _lognormal_sample(n, mu=0.0, sigma=0.7, rng=None):
    rng = rng or np.random.default_rng(42)
    return np.exp(rng.normal(mu, sigma, n))


@poi_style(size=FIG_FULL)
def fig_center_compared():
    """Skewed distribution with mean, median, mode marked."""
    fig, ax = plt.subplots()
    rng = np.random.default_rng(11)
    data = _lognormal_sample(20000, 0.0, 0.7, rng)

    # Histogram density
    ax.hist(data, bins=80, range=(0, 6), density=True,
            color=DIM, alpha=0.45, edgecolor="white", linewidth=0.4)

    # Theoretical lognormal density for smooth overlay
    x = np.linspace(0.01, 6, 600)
    sigma, mu = 0.7, 0.0
    y = (1 / (x * sigma * np.sqrt(2 * np.pi))) * np.exp(
        -((np.log(x) - mu) ** 2) / (2 * sigma ** 2)
    )
    ax.plot(x, y, color=INK, linewidth=1.6)

    # Compute the three centers
    mean = np.mean(data)
    median = np.median(data)
    # Mode: location of max of theoretical density
    mode = np.exp(mu - sigma ** 2)

    ymax = ax.get_ylim()[1]
    ax.axvline(mode, color=SAGE, linewidth=2.0, label=f"mode ≈ {mode:.2f}")
    ax.axvline(median, color=GOLD, linewidth=2.0, label=f"median ≈ {median:.2f}")
    ax.axvline(mean, color=RUST, linewidth=2.0, label=f"mean ≈ {mean:.2f}")

    ax.set_xlim(0, 6)
    ax.set_ylim(0, ymax)
    ax.set_xlabel("value")
    ax.set_ylabel("density")
    ax.set_title("Three centers of a right-skewed distribution",
                 fontsize=11)
    ax.legend(frameon=False, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=(8.5, 4))
def fig_spread_compared():
    """Three normals with same mean, different sd."""
    fig, ax = plt.subplots()
    x = np.linspace(-8, 8, 600)
    sds = [0.5, 1.0, 2.5]
    colors = [INK, GOLD, RUST]
    for sd, color in zip(sds, colors):
        y = (1 / (sd * np.sqrt(2 * np.pi))) * np.exp(-x ** 2 / (2 * sd ** 2))
        ax.plot(x, y, color=color, linewidth=1.6,
                label=f"sd = {sd},  IQR ≈ {1.349 * sd:.2f}")
        ax.fill_between(x, 0, y, color=color, alpha=0.10)
    ax.set_xlim(-8, 8)
    ax.set_xlabel("value")
    ax.set_ylabel("density")
    ax.set_title("Same center, three different spreads", fontsize=11)
    ax.legend(frameon=False, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=(8.5, 5))
def fig_shapes():
    """Four-panel: symmetric, right-skewed, heavy-tailed, bimodal."""
    fig, axes = plt.subplots(2, 2, figsize=(8.5, 5))
    rng = np.random.default_rng(123)

    # Symmetric (normal)
    ax = axes[0, 0]
    x = np.linspace(-4, 4, 500)
    ax.plot(x, np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi),
            color=INK, linewidth=1.6)
    ax.fill_between(x, 0, np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi),
                    color=INK, alpha=0.15)
    ax.set_title("Symmetric (normal)", fontsize=10)

    # Right-skewed (log-normal)
    ax = axes[0, 1]
    x = np.linspace(0.01, 6, 500)
    sigma = 0.7
    y = (1 / (x * sigma * np.sqrt(2 * np.pi))) * np.exp(-(np.log(x)) ** 2 / (2 * sigma ** 2))
    ax.plot(x, y, color=RUST, linewidth=1.6)
    ax.fill_between(x, 0, y, color=RUST, alpha=0.15)
    ax.set_title("Right-skewed (log-normal)", fontsize=10)

    # Heavy-tailed (t with df=2)
    ax = axes[1, 0]
    from math import gamma as G
    df = 2
    x = np.linspace(-6, 6, 500)
    c = G((df + 1) / 2) / (np.sqrt(df * np.pi) * G(df / 2))
    y = c * (1 + x ** 2 / df) ** (-(df + 1) / 2)
    ax.plot(x, y, color=GOLD, linewidth=1.6)
    ax.fill_between(x, 0, y, color=GOLD, alpha=0.15)
    # Compare to normal
    yn = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(x, yn, color=DIM, linewidth=1.0, linestyle="dashed",
            label="normal")
    ax.set_title("Heavy-tailed (t, df=2)", fontsize=10)
    ax.legend(frameon=False, loc="upper right", fontsize=8)

    # Bimodal
    ax = axes[1, 1]
    x = np.linspace(-6, 6, 500)
    y = 0.5 * np.exp(-(x + 2) ** 2 / 1.5) / np.sqrt(1.5 * np.pi) + \
        0.5 * np.exp(-(x - 2) ** 2 / 1.5) / np.sqrt(1.5 * np.pi)
    ax.plot(x, y, color=VIOLET, linewidth=1.6)
    ax.fill_between(x, 0, y, color=VIOLET, alpha=0.15)
    ax.set_title("Bimodal (mixture of two normals)", fontsize=10)

    for ax in axes.flatten():
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_yticks([])
        ax.grid(True, alpha=0.25)

    plt.tight_layout()
    return fig


@poi_style(size=(8.5, 4))
def fig_robustness():
    """Mean vs median when an outlier is added."""
    rng = np.random.default_rng(7)
    base = rng.normal(0, 1, 50)
    outlier = 100.0
    with_outlier = np.append(base, outlier)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))

    for ax, data, title in zip(
        axes,
        [base, with_outlier],
        ["50 points around 0 (no outlier)",
         "Same 50 points + one outlier at 100"],
    ):
        m = np.mean(data)
        med = np.median(data)
        sd = np.std(data, ddof=1)
        # Plot the points (jittered)
        y_jit = rng.uniform(-0.05, 0.05, len(data))
        # Use clipping x-axis so outlier is visible
        ax.scatter(data, y_jit, s=15, color=INK, alpha=0.5)
        ax.axvline(m, color=RUST, linewidth=2.0, label=f"mean = {m:.2f}")
        ax.axvline(med, color=SAGE, linewidth=2.0, label=f"median = {med:.2f}")
        ax.set_xlim(-4, 105)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_title(title + f"\n(sd = {sd:.2f})", fontsize=9)
        ax.legend(frameon=False, fontsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=(9, 5))
def fig_boxplot():
    """Boxplot anatomy + 4 distribution shapes as boxplots."""
    rng = np.random.default_rng(2026)

    fig = plt.figure(figsize=(9, 5))
    gs = fig.add_gridspec(1, 5, width_ratios=[2, 1, 1, 1, 1])

    # Panel 1: anatomy
    ax = fig.add_subplot(gs[0, 0])
    sample = rng.normal(0, 1, 300)
    bp = ax.boxplot(sample, vert=True, widths=0.5, patch_artist=True,
                    boxprops=dict(facecolor=INK, alpha=0.3, edgecolor=INK),
                    medianprops=dict(color=RUST, linewidth=2.0),
                    whiskerprops=dict(color=INK),
                    capprops=dict(color=INK),
                    flierprops=dict(marker="o", markerfacecolor=DIM,
                                    markersize=4, markeredgecolor="none"))
    # Annotations
    q1, med, q3 = np.percentile(sample, [25, 50, 75])
    ax.annotate("median", xy=(1.25, med), xytext=(1.7, med),
                arrowprops=dict(arrowstyle="-", color=RUST), fontsize=9,
                color=RUST, va="center")
    ax.annotate("Q1 (25th pct)", xy=(1.25, q1), xytext=(1.7, q1 - 0.4),
                arrowprops=dict(arrowstyle="-", color=INK), fontsize=9,
                color=INK, va="center")
    ax.annotate("Q3 (75th pct)", xy=(1.25, q3), xytext=(1.7, q3 + 0.4),
                arrowprops=dict(arrowstyle="-", color=INK), fontsize=9,
                color=INK, va="center")
    ax.annotate("whisker\n(non-outlier max)",
                xy=(1.0, np.max(sample[sample < q3 + 1.5 * (q3 - q1)])),
                xytext=(1.6, 2.5),
                arrowprops=dict(arrowstyle="-", color=DIM), fontsize=9,
                color=DIM, va="center")
    ax.set_xlim(0.5, 3.2)
    ax.set_xticks([])
    ax.set_title("Boxplot anatomy", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Panels 2-5: four distributions
    titles = ["normal", "right-skew", "heavy-tail", "bimodal"]
    samples = [
        rng.normal(0, 1, 400),
        np.exp(rng.normal(0, 0.7, 400)),
        rng.standard_t(2, 400),
        np.concatenate([rng.normal(-2, 0.7, 200),
                        rng.normal(2, 0.7, 200)]),
    ]
    colors_set = [INK, RUST, GOLD, VIOLET]

    for i, (title, sample, color) in enumerate(zip(titles, samples, colors_set)):
        ax = fig.add_subplot(gs[0, i + 1])
        ax.boxplot(sample, vert=True, widths=0.6, patch_artist=True,
                   boxprops=dict(facecolor=color, alpha=0.3, edgecolor=color),
                   medianprops=dict(color="black", linewidth=1.8),
                   whiskerprops=dict(color=color),
                   capprops=dict(color=color),
                   flierprops=dict(marker="o", markerfacecolor=DIM,
                                   markersize=3, markeredgecolor="none"))
        ax.set_xticks([])
        ax.set_title(title, fontsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig
