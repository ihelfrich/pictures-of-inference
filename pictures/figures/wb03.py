"""Figures for Workbook 3: Hypothesis testing in practice."""
from poi import poi_style, INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL, FIG_FULL
import matplotlib.pyplot as plt
import numpy as np
from math import gamma as gamma_func, erf


def _t_pdf(x, df):
    c = gamma_func((df + 1) / 2) / (np.sqrt(df * np.pi) * gamma_func(df / 2))
    return c * (1 + x ** 2 / df) ** (-(df + 1) / 2)


def _norm_pdf(x, mu=0, sd=1):
    return (1 / (sd * np.sqrt(2 * np.pi))) * np.exp(-((x - mu) ** 2) / (2 * sd ** 2))


@poi_style(size=FIG_FULL)
def fig_wb3_q1():
    """One-sample t-test: sampling distribution of the mean under H0."""
    fig, ax = plt.subplots()
    se = 4.5 / np.sqrt(25)
    x = np.linspace(95, 106, 500)
    y = _norm_pdf(x, mu=100, sd=se)
    ax.plot(x, y, color=INK, linewidth=1.8)
    # Critical regions (two-sided 0.05): mu_0 ± t_crit * se
    t_crit = 2.064  # df = 24, alpha/2 = 0.025
    ax.fill_between(x, 0, y, where=(x <= 100 - t_crit * se),
                    color=RUST, alpha=0.4, label="rejection region")
    ax.fill_between(x, 0, y, where=(x >= 100 + t_crit * se),
                    color=RUST, alpha=0.4)
    ax.axvline(102.3, color=GOLD, linewidth=2.0,
               label="observed mean = 102.3")
    ax.axvline(100, color=DIM, linestyle="dotted", linewidth=1.0,
               label=r"$\mu_0$ = 100")
    ax.set_xlabel("sample mean (g)")
    ax.set_ylabel("density")
    ax.set_title("Sampling distribution of $\\bar{X}$ under $H_0: \\mu = 100$",
                 fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb3_q2():
    """Two-sample t-test: overlapping sampling distributions."""
    rng = np.random.default_rng(302)
    fig, ax = plt.subplots()
    x = np.linspace(125, 165, 500)
    se_d = 12 / np.sqrt(40)
    se_p = 14 / np.sqrt(40)
    ax.plot(x, _norm_pdf(x, mu=138, sd=se_d), color=INK, linewidth=1.8,
            label="drug ($\\bar{x}_D$ = 138, $s_D$ = 12)")
    ax.fill_between(x, 0, _norm_pdf(x, mu=138, sd=se_d), color=INK, alpha=0.18)
    ax.plot(x, _norm_pdf(x, mu=145, sd=se_p), color=RUST, linewidth=1.8,
            label="placebo ($\\bar{x}_P$ = 145, $s_P$ = 14)")
    ax.fill_between(x, 0, _norm_pdf(x, mu=145, sd=se_p), color=RUST, alpha=0.18)
    ax.set_xlabel("systolic BP (mmHg)")
    ax.set_ylabel("density")
    ax.set_title("Sampling distributions of the two group means", fontsize=11)
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb3_q3():
    """Paired-difference histogram."""
    rng = np.random.default_rng(303)
    n = 30
    deltas = rng.normal(loc=-8, scale=14, size=n)
    fig, ax = plt.subplots()
    ax.hist(deltas, bins=12, color=SAGE, alpha=0.8,
            edgecolor="white", linewidth=0.6)
    ax.axvline(0, color=DIM, linestyle="dashed", linewidth=1.0,
               label="no change")
    ax.axvline(np.mean(deltas), color=RUST, linewidth=2.0,
               label=f"observed mean = {np.mean(deltas):+.1f}")
    ax.set_xlabel("post − pre cholesterol (mg/dL)")
    ax.set_ylabel("count")
    ax.set_title("Within-subject changes after 8-week intervention", fontsize=11)
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb3_q4():
    """Proportion test: sampling distribution under H0."""
    fig, ax = plt.subplots()
    p0 = 0.02
    n = 500
    se = np.sqrt(p0 * (1 - p0) / n)
    x = np.linspace(0, 0.05, 500)
    y = _norm_pdf(x, mu=p0, sd=se)
    ax.plot(x, y, color=INK, linewidth=1.8)
    z_crit = 1.645
    ax.fill_between(x, 0, y, where=(x >= p0 + z_crit * se),
                    color=RUST, alpha=0.4,
                    label=f"rejection region (one-sided, α=0.05)")
    ax.axvline(0.028, color=GOLD, linewidth=2.0,
               label="observed = 0.028")
    ax.axvline(p0, color=DIM, linestyle="dotted", linewidth=1.0,
               label="$p_0$ = 0.02")
    ax.set_xlabel("sample proportion of defects")
    ax.set_ylabel("density")
    ax.set_title("Sampling distribution of $\\hat{p}$ under $H_0: p = 0.02$",
                 fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=(10, 4.5))
def fig_wb3_q5():
    """Chi-squared: mosaic plot + cell residuals."""
    # Hypothetical 3x3 contingency table
    obs = np.array([
        [120,  60,  20],   # Dem
        [ 50, 110,  40],   # Rep
        [ 80, 130, 190],   # Ind  (yes, large)
    ], dtype=float)
    rownames = ["Dem", "Rep", "Ind"]
    colnames = ["TV", "Web", "Print"]
    n = obs.sum()
    row_tot = obs.sum(axis=1, keepdims=True)
    col_tot = obs.sum(axis=0, keepdims=True)
    expected = row_tot @ col_tot / n
    std_resid = (obs - expected) / np.sqrt(expected)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # Left: mosaic-style
    ax = axes[0]
    x_left = 0.0
    for i, rn in enumerate(rownames):
        col_w = row_tot[i, 0] / n
        y_bot = 0.0
        for j, cn in enumerate(colnames):
            cell_h = obs[i, j] / row_tot[i, 0]
            color = [INK, RUST, SAGE][j]
            ax.add_patch(plt.Rectangle((x_left, y_bot), col_w - 0.005,
                                        cell_h - 0.005,
                                        facecolor=color, alpha=0.75,
                                        edgecolor="white", linewidth=1.2))
            ax.text(x_left + col_w / 2, y_bot + cell_h / 2,
                    f"{int(obs[i,j])}", ha="center", va="center",
                    color="white", fontweight="bold", fontsize=9)
            y_bot += cell_h
        ax.text(x_left + col_w / 2, -0.04, rn, ha="center", va="top",
                fontsize=10, color=INK, fontweight="bold")
        x_left += col_w
    # Column legend
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=c, alpha=0.75)
               for c in [INK, RUST, SAGE]]
    ax.legend(handles, colnames, loc="upper center",
              bbox_to_anchor=(0.5, -0.10), ncol=3, frameon=False)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.10, 1.02)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Mosaic plot of observed counts", fontsize=11)
    for s in ax.spines.values():
        s.set_visible(False)

    # Right: standardized residuals heatmap
    ax = axes[1]
    im = ax.imshow(std_resid, cmap="RdBu_r", vmin=-5, vmax=5,
                   aspect="auto")
    ax.set_xticks(range(len(colnames)))
    ax.set_xticklabels(colnames)
    ax.set_yticks(range(len(rownames)))
    ax.set_yticklabels(rownames)
    for i in range(len(rownames)):
        for j in range(len(colnames)):
            ax.text(j, i, f"{std_resid[i,j]:+.1f}",
                    ha="center", va="center",
                    color="white" if abs(std_resid[i, j]) > 2.5 else "black",
                    fontsize=10)
    fig.colorbar(im, ax=ax, label="standardized residual")
    ax.set_title("Cell-level deviations from independence", fontsize=11)

    plt.tight_layout()
    return fig


@poi_style(size=FIG_FULL)
def fig_wb3_q6():
    """Power curve as a function of sample size."""
    fig, ax = plt.subplots()
    p0, p1 = 0.02, 0.03
    z_alpha = 1.645
    ns = np.arange(50, 4000, 50)
    se0 = np.sqrt(p0 * (1 - p0) / ns)
    se1 = np.sqrt(p1 * (1 - p1) / ns)
    # Power approx: P(p_hat > p0 + z_alpha*se0 | p_1)
    z = (p0 + z_alpha * se0 - p1) / se1
    power = 1 - 0.5 * (1 + np.array([erf(zi / np.sqrt(2)) for zi in z]))
    ax.plot(ns, power, color=INK, linewidth=2.0)
    ax.axhline(0.80, color=DIM, linestyle="dashed", linewidth=1.0,
               label="80% power target")
    # Find n where power crosses 0.80
    idx = np.argmin(np.abs(power - 0.80))
    ax.axvline(ns[idx], color=RUST, linestyle="dotted", linewidth=1.4)
    ax.scatter([ns[idx]], [power[idx]], s=80, color=RUST, zorder=5,
               label=f"n ≈ {ns[idx]}")
    ax.set_xlabel("sample size n")
    ax.set_ylabel("power to reject $H_0$")
    ax.set_title("Power to detect 3% defect rate vs null of 2%, α = 0.05",
                 fontsize=11)
    ax.legend(frameon=False)
    ax.set_ylim(0, 1.05)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb3_q7():
    """Histogram of 100 p-values under all-true-null simulation."""
    rng = np.random.default_rng(307)
    p_values = rng.uniform(0, 1, 100)
    fig, ax = plt.subplots()
    ax.hist(p_values, bins=20, color=INK, alpha=0.8,
            edgecolor="white", linewidth=0.5)
    ax.axvline(0.05, color=RUST, linestyle="dashed", linewidth=1.5,
               label="α = 0.05")
    n_signif = (p_values < 0.05).sum()
    ax.set_xlabel("p-value")
    ax.set_ylabel("count")
    ax.set_title(f"100 hypothesis tests, all nulls true. "
                 f"{n_signif} would 'reject' at α=0.05",
                 fontsize=11)
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig
