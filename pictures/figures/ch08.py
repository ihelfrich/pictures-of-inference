"""
Figures for Chapter 8: Visualizing uncertainty.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_FULL, FIG_SPREAD,
)
import matplotlib.pyplot as plt
import numpy as np


@poi_style(size=(9, 5.5))
def fig_conf_band():
    """Linear regression with 95% confidence band."""
    rng = np.random.default_rng(2026)
    n = 60
    x = np.sort(rng.uniform(0, 30, n))
    true_slope = 0.85
    y = 0.5 + true_slope * x + rng.normal(0, 2.5, n)

    # OLS
    X = np.column_stack([np.ones(n), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    yhat = X @ beta
    resid = y - yhat
    sigma2 = (resid @ resid) / (n - 2)
    XtXinv = np.linalg.inv(X.T @ X)

    grid = np.linspace(x.min() - 4, x.max() + 4, 200)
    Xg = np.column_stack([np.ones_like(grid), grid])
    yhat_g = Xg @ beta
    se_g = np.sqrt(np.einsum("ij,jk,ik->i", Xg, XtXinv, Xg) * sigma2)
    lo = yhat_g - 1.96 * se_g
    hi = yhat_g + 1.96 * se_g

    fig, ax = plt.subplots()
    ax.fill_between(grid, lo, hi, color=GOLD, alpha=0.35,
                    label="95% confidence band")
    ax.plot(grid, yhat_g, color=INK, linewidth=2,
            label=f"fitted line: y = {beta[0]:.2f} + {beta[1]:.2f}x")
    ax.scatter(x, y, s=22, color=INK, alpha=0.7,
               edgecolor="white", linewidth=0.5,
               label=f"observations (n = {n})")
    ax.set_xlabel("importer GDP (USD trillions, simulated)")
    ax.set_ylabel("bilateral exports (simulated, USD billions)")
    ax.set_title("Confidence band: where the regression line plausibly lies",
                 fontsize=12)
    ax.legend(frameon=False, loc="upper left")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_coef_plot():
    """Coefficient plot of a multiple regression."""
    coefs = [
        ("intercept",       -3.60, 0.45),
        ("log GDP exporter", 0.95, 0.07),
        ("log GDP importer", 0.85, 0.08),
        ("log distance",    -0.85, 0.10),
        ("common language",  0.40, 0.13),
        ("common border",    0.30, 0.18),
    ]
    names = [c[0] for c in coefs]
    point = np.array([c[1] for c in coefs])
    se = np.array([c[2] for c in coefs])
    lo = point - 1.96 * se
    hi = point + 1.96 * se

    fig, ax = plt.subplots()
    ys = np.arange(len(coefs))[::-1]
    for i, (y, p, l, h) in enumerate(zip(ys, point, lo, hi)):
        crosses_zero = (l < 0) and (h > 0)
        color = DIM if crosses_zero else INK
        ax.plot([l, h], [y, y], color=color, linewidth=2.0)
        ax.scatter([p], [y], s=80, color=color, zorder=3,
                   edgecolor="white", linewidth=1.5)
    ax.axvline(0, color=RUST, linestyle="dashed", linewidth=1, alpha=0.7,
               label="null at 0")
    ax.set_yticks(ys)
    ax.set_yticklabels(names)
    ax.set_xlabel("coefficient (95% interval)")
    ax.set_title("Coefficient plot: gravity-model regression on log exports",
                 fontsize=12)
    ax.legend(frameon=False, loc="lower right")
    ax.grid(True, axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=(9, 5.5))
def fig_hop():
    """Hypothetical outcome plot: 20 sampled regression lines."""
    rng = np.random.default_rng(11)
    n = 60
    x = np.sort(rng.uniform(0, 30, n))
    y = 0.5 + 0.85 * x + rng.normal(0, 2.8, n)
    X = np.column_stack([np.ones(n), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    yhat = X @ beta
    resid = y - yhat
    sigma2 = (resid @ resid) / (n - 2)
    XtXinv = np.linalg.inv(X.T @ X)
    cov = sigma2 * XtXinv
    L = np.linalg.cholesky(cov)

    grid = np.linspace(x.min() - 2, x.max() + 2, 200)
    Xg = np.column_stack([np.ones_like(grid), grid])

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=22, color=INK, alpha=0.5,
               edgecolor="white", linewidth=0.5)

    # 20 draws from beta distribution
    for k in range(20):
        z = rng.standard_normal(2)
        b = beta + L @ z
        ax.plot(grid, Xg @ b, color=VIOLET, alpha=0.30, linewidth=1.0)
    # Central estimate
    ax.plot(grid, Xg @ beta, color=INK, linewidth=2.5,
            label="central estimate")

    ax.set_xlabel("importer GDP (USD trillions, simulated)")
    ax.set_ylabel("bilateral exports (simulated, USD billions)")
    ax.set_title("Hypothetical outcome plot: 20 sampled regression lines",
                 fontsize=12)
    ax.legend(frameon=False, loc="upper left")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_fan_chart():
    """Fan chart: forecast with nested prediction intervals."""
    rng = np.random.default_rng(7)
    n_obs = 30
    n_fore = 24
    t_obs = np.arange(n_obs)
    t_fore = np.arange(n_obs, n_obs + n_fore)
    obs = 50 + 0.6 * t_obs + rng.normal(0, 2.5, n_obs)
    last = obs[-1]
    drift = 0.6
    forecast = last + drift * (t_fore - t_obs[-1])
    sd_t = 2.5 * np.sqrt(1 + (t_fore - t_obs[-1]) * 0.6)

    levels = [0.50, 0.80, 0.95]
    z_for = {0.50: 0.674, 0.80: 1.282, 0.95: 1.960}
    colors = {0.50: GOLD, 0.80: SAGE, 0.95: TEAL}

    fig, ax = plt.subplots()
    for level in sorted(levels, reverse=True):
        z = z_for[level]
        lo = forecast - z * sd_t
        hi = forecast + z * sd_t
        ax.fill_between(t_fore, lo, hi,
                        color=colors[level], alpha=0.30,
                        label=f"{int(level * 100)}% interval")
    ax.plot(t_obs, obs, color=INK, linewidth=2, marker="o",
            markersize=4, label="observed")
    ax.plot(t_fore, forecast, color=INK, linewidth=2,
            linestyle="dashed", label="point forecast")
    ax.axvline(t_obs[-1], color=DIM, linestyle="dotted", linewidth=1)
    ax.text(t_obs[-1], ax.get_ylim()[0] + 1.5, " forecast →",
            fontsize=9, color=DIM)
    ax.set_xlabel("time")
    ax.set_ylabel("value")
    ax.set_title("Fan chart: nested prediction intervals widening with horizon",
                 fontsize=12)
    ax.legend(frameon=False, loc="upper left")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=(9, 5.5))
def fig_show_all():
    """Show all data: scatter + smoothed conditional mean."""
    rng = np.random.default_rng(2026)
    n = 300
    x = rng.uniform(0, 30, n)
    y = 0.5 + 0.85 * x + rng.normal(0, np.sqrt(1 + x) * 0.8, n)

    # Smoothed conditional mean: simple moving average over sorted x
    order = np.argsort(x)
    x_s = x[order]
    y_s = y[order]
    window = 25
    smooth = np.array([
        y_s[max(0, i - window // 2): min(n, i + window // 2)].mean()
        for i in range(n)
    ])

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=18, color=INK, alpha=0.45,
               edgecolor="white", linewidth=0.4,
               label=f"all {n} observations")
    ax.plot(x_s, smooth, color=RUST, linewidth=2.5,
            label="smoothed conditional mean")
    ax.set_xlabel("importer GDP (USD trillions, simulated)")
    ax.set_ylabel("bilateral exports (simulated, USD billions)")
    ax.set_title("Show all the data: 300 points and a smoothed mean",
                 fontsize=12)
    ax.legend(frameon=False, loc="upper left")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig
