"""Figures for Workbook 1: Distributions in the wild."""
from poi import poi_style, INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL, FIG_FULL
import matplotlib.pyplot as plt
import numpy as np


def _hist(ax, data, bins, color=INK, xlabel="", title=""):
    ax.hist(data, bins=bins, color=color, alpha=0.85,
            edgecolor="white", linewidth=0.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("count")
    ax.set_title(title, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


@poi_style(size=FIG_FULL)
def fig_wb1_q1():
    rng = np.random.default_rng(101)
    data = rng.normal(loc=175, scale=7, size=1000)
    fig, ax = plt.subplots()
    _hist(ax, data, bins=35, color=INK,
          xlabel="height (cm)", title="1,000 adult heights")
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q2():
    rng = np.random.default_rng(102)
    data = rng.exponential(scale=10.0, size=500)
    fig, ax = plt.subplots()
    _hist(ax, data, bins=40, color=RUST,
          xlabel="wait time (minutes)", title="500 bus stop wait times")
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q3():
    rng = np.random.default_rng(103)
    data = rng.poisson(lam=2.5, size=200)
    fig, ax = plt.subplots()
    bins = np.arange(0, max(data) + 2) - 0.5
    _hist(ax, data, bins=bins, color=SAGE,
          xlabel="typos per page", title="200 pages, typo counts")
    ax.set_xticks(np.arange(0, max(data) + 1))
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q4():
    rng = np.random.default_rng(104)
    data = rng.lognormal(mean=np.log(55), sigma=0.6, size=5000)
    fig, ax = plt.subplots()
    _hist(ax, data[data < 400], bins=60, color=GOLD,
          xlabel="annual income (USD thousands)",
          title="5,000 household incomes")
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q5():
    rng = np.random.default_rng(105)
    data = rng.binomial(n=20, p=0.5, size=1000)
    fig, ax = plt.subplots()
    bins = np.arange(0, 22) - 0.5
    _hist(ax, data, bins=bins, color=INK,
          xlabel="number of heads in 20 flips",
          title="1,000 repetitions of 20 coin flips")
    ax.set_xticks(np.arange(0, 21, 2))
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q6():
    rng = np.random.default_rng(106)
    # Heavy-tailed via mixture: mostly normal, but with heavy fraction
    n = 5000
    main = rng.normal(loc=0.0, scale=0.8, size=int(0.95 * n))
    tail = rng.standard_t(df=3, size=n - int(0.95 * n)) * 1.5
    data = np.concatenate([main, tail])
    fig, ax = plt.subplots()
    _hist(ax, data[(data > -8) & (data < 8)], bins=80, color=RUST,
          xlabel="daily return (%)",
          title="5,000 daily stock returns")
    # Overlay normal for comparison
    x = np.linspace(-8, 8, 400)
    sd = data.std()
    norm_curve = (1 / (sd * np.sqrt(2 * np.pi))) * np.exp(-x ** 2 / (2 * sd ** 2))
    # Scale to histogram bin widths
    bin_width = 16 / 80
    ax.plot(x, norm_curve * len(data) * bin_width, color=DIM,
            linestyle="dashed", linewidth=1.2, label="normal reference")
    ax.legend(frameon=False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q7():
    rng = np.random.default_rng(107)
    data = rng.lognormal(mean=np.log(380), sigma=0.5, size=800)
    fig, ax = plt.subplots()
    _hist(ax, data[data < 1500], bins=50, color=VIOLET,
          xlabel="reaction time (ms)",
          title="800 reaction-time trials")
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q8():
    """Use the actual trade slice, plotted log-scale."""
    from poi.data import trade
    rows = trade()
    exports = np.array([r["exports_usd_millions"] for r in rows])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    _hist(axes[0], exports, bins=40, color=INK,
          xlabel="exports (USD millions)",
          title="Linear scale: 300 bilateral observations")
    _hist(axes[1], np.log(exports), bins=40, color=TEAL,
          xlabel="log(exports)",
          title="Log scale: same 300 observations")
    plt.tight_layout()
    return fig


@poi_style(size=(10, 4.5))
def fig_wb1_q9():
    """UK house prices: linear vs log scale histograms."""
    import pandas as pd
    rng = np.random.default_rng(901)
    df = pd.read_parquet('/Volumes/HELFRICH-GD/UK_EconomicData/data/raw/LandRegistry_PPD_Latest.parquet')
    prices = df['price'].values
    prices = prices[prices < 2_000_000]          # drop extreme outliers
    sample = rng.choice(prices, size=8000, replace=False)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].hist(sample / 1000, bins=60, color=INK, alpha=0.85,
                 edgecolor='white', linewidth=0.5)
    axes[0].set_xlabel('transaction price (£ thousands)')
    axes[0].set_ylabel('count')
    axes[0].set_title('Linear scale: 8,000 transactions', fontsize=11)
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)

    axes[1].hist(np.log(sample), bins=60, color=TEAL, alpha=0.85,
                 edgecolor='white', linewidth=0.5)
    axes[1].set_xlabel('log(transaction price)')
    axes[1].set_ylabel('count')
    axes[1].set_title('Log scale: same 8,000 transactions', fontsize=11)
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)

    plt.tight_layout()
    return fig


@poi_style(size=FIG_FULL)
def fig_wb1_q10():
    """IMD 2019: distribution of deprivation scores across English LSOAs."""
    import pandas as pd
    df = pd.read_parquet('/Volumes/HELFRICH-GD/UK_EconomicData/data/raw/IMD_2019_England.parquet')
    scores = df['Index of Multiple Deprivation (IMD) Score'].values

    fig, ax = plt.subplots()
    ax.hist(scores, bins=60, color=RUST, alpha=0.85,
            edgecolor='white', linewidth=0.5)
    mean_v = scores.mean()
    median_v = np.median(scores)
    ax.axvline(mean_v, color=GOLD, linewidth=2.0,
               label=f'mean = {mean_v:.1f}')
    ax.axvline(median_v, color=SAGE, linewidth=2.0, linestyle='dashed',
               label=f'median = {median_v:.1f}')
    ax.set_xlabel('IMD score (England, 2019)')
    ax.set_ylabel('count')
    ax.set_title('Deprivation scores across 32,844 English LSOAs', fontsize=11)
    ax.legend(frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig
