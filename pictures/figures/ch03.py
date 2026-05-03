"""
Figures for Chapter 3: Shapes of data.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_SINGLE, FIG_FULL, FIG_SPREAD,
)
import matplotlib.pyplot as plt
import numpy as np
from math import factorial


@poi_style(size=(7.5, 5.5))
def fig_bernoulli_binomial():
    """Top row: Bernoulli at three p values. Bottom: Binomial(20, p) at the same."""
    fig, axes = plt.subplots(2, 3, figsize=(8, 5))

    ps = [0.2, 0.5, 0.8]
    n = 20

    # Top row: Bernoulli
    for i, p in enumerate(ps):
        ax = axes[0, i]
        ax.bar([0, 1], [1 - p, p], width=0.5,
               color=[DIM, INK], edgecolor="white", linewidth=1.5)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["0", "1"])
        ax.set_ylim(0, 1)
        ax.set_title(f"Bernoulli, p = {p}", fontsize=10)
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if i == 0:
            ax.set_ylabel("probability")

    # Bottom row: Binomial(20, p)
    ks = np.arange(0, n + 1)
    for i, p in enumerate(ps):
        ax = axes[1, i]
        # Compute binomial PMF directly
        pmf = np.array([
            (factorial(n) // (factorial(k) * factorial(n - k))) *
            p ** k * (1 - p) ** (n - k)
            for k in ks
        ])
        ax.bar(ks, pmf, width=0.85, color=INK, edgecolor="white", linewidth=0.5)
        ax.set_title(f"Binomial(20, {p})", fontsize=10)
        ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(0, max(pmf) * 1.15)
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if i == 0:
            ax.set_ylabel("probability")
        ax.set_xlabel("k (number of yeses)")

    plt.tight_layout()
    return fig


@poi_style(size=FIG_FULL)
def fig_poisson():
    """Poisson PMF at three values of lambda."""
    fig, ax = plt.subplots()
    lambdas = [1.0, 4.0, 10.0]
    colors = [INK, RUST, SAGE]
    ks = np.arange(0, 25)
    for lam, color in zip(lambdas, colors):
        # Poisson PMF
        pmf = np.exp(-lam) * lam ** ks / np.array([factorial(k) for k in ks])
        ax.plot(ks, pmf, "o-", color=color, markersize=6, linewidth=1.5,
                label=fr"$\lambda = {lam}$")

    ax.set_xlabel("k")
    ax.set_ylabel("P(K = k)")
    ax.set_title("Poisson distributions at three rates", fontsize=11)
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.3)
    return fig


@poi_style(size=FIG_FULL)
def fig_normal_68_95_99():
    """Standard normal with 68-95-99.7 bands."""
    fig, ax = plt.subplots()
    x = np.linspace(-4, 4, 600)
    y = (1 / np.sqrt(2 * np.pi)) * np.exp(-x ** 2 / 2)

    # Bands (outermost first so inner ones layer on top)
    ax.fill_between(x, 0, y, where=(np.abs(x) <= 3),
                    color=DIM, alpha=0.25, label="99.7%")
    ax.fill_between(x, 0, y, where=(np.abs(x) <= 2),
                    color=GOLD, alpha=0.45, label="95%")
    ax.fill_between(x, 0, y, where=(np.abs(x) <= 1),
                    color=INK, alpha=0.55, label="68%")
    ax.plot(x, y, color=INK, linewidth=1.4)

    # Mark sigma multiples
    for k in [-3, -2, -1, 1, 2, 3]:
        ax.axvline(k, color=DIM, linestyle="dotted", linewidth=0.8, alpha=0.7)
        ax.text(k, -0.012, fr"${k:+d}\sigma$", ha="center", va="top",
                fontsize=9, color=DIM)

    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.025, 0.45)
    ax.set_xlabel(r"value (in units of $\sigma$)")
    ax.set_ylabel("density")
    ax.set_title("The standard normal: 68-95-99.7", fontsize=11)
    ax.legend(loc="upper right", frameon=False)
    return fig


@poi_style(size=(8.5, 4))
def fig_exp_lognormal():
    """Exponential and log-normal side by side."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4))

    # Exponential, rate 1
    x = np.linspace(0, 6, 500)
    y_exp = np.exp(-x)
    ax1.plot(x, y_exp, color=INK, linewidth=1.6)
    ax1.fill_between(x, 0, y_exp, color=INK, alpha=0.18)
    ax1.set_title("Exponential (rate 1):  story = waiting", fontsize=10)
    ax1.set_xlabel("wait time")
    ax1.set_ylabel("density")
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 1.1)

    # Log-normal, mu=0, sigma=0.7
    mu, sigma = 0.0, 0.7
    x2 = np.linspace(0.01, 8, 500)
    y_ln = (1 / (x2 * sigma * np.sqrt(2 * np.pi))) * np.exp(
        -((np.log(x2) - mu) ** 2) / (2 * sigma ** 2)
    )
    ax2.plot(x2, y_ln, color=RUST, linewidth=1.6)
    ax2.fill_between(x2, 0, y_ln, color=RUST, alpha=0.18)
    ax2.set_title(r"Log-normal ($\mu=0,\sigma=0.7$):  story = multiplied",
                  fontsize=10)
    ax2.set_xlabel("value")
    ax2.set_xlim(0, 8)
    ax2.set_ylim(0, 0.6)

    for ax in (ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=FIG_FULL)
def fig_t_vs_normal():
    """Student's t at multiple df overlaid on the standard normal."""
    fig, ax = plt.subplots()
    x = np.linspace(-5, 5, 600)
    # Standard normal
    y_norm = (1 / np.sqrt(2 * np.pi)) * np.exp(-x ** 2 / 2)
    ax.plot(x, y_norm, color="black", linewidth=2.0, label="Normal")

    # t distributions at several df
    from math import gamma as gamma_func
    dfs = [2, 10, 30]
    colors = [RUST, GOLD, SAGE]
    for df, color in zip(dfs, colors):
        c = (gamma_func((df + 1) / 2)
             / (np.sqrt(df * np.pi) * gamma_func(df / 2)))
        y_t = c * (1 + x ** 2 / df) ** (-(df + 1) / 2)
        ax.plot(x, y_t, color=color, linewidth=1.4,
                label=f"t, df = {df}")

    ax.set_xlim(-5, 5)
    ax.set_xlabel("value")
    ax.set_ylabel("density")
    ax.set_title("Student's t vs. the standard normal", fontsize=11)
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.25)
    return fig
