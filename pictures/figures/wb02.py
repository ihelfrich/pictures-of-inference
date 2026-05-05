"""Figures for Workbook 2: Reading regressions by inspection."""
from poi import poi_style, INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL, FIG_FULL
import matplotlib.pyplot as plt
import numpy as np


def _scatter(ax, x, y, line_x=None, line_y=None,
             ref_y=None, color=INK, label_pts=None):
    ax.scatter(x, y, s=30, color=color, alpha=0.6,
               edgecolor="white", linewidth=0.5)
    if line_x is not None and line_y is not None:
        ax.plot(line_x, line_y, color=RUST, linewidth=1.8,
                label="OLS fit")
    if ref_y is not None:
        ax.plot(line_x if line_x is not None else x,
                ref_y, color=DIM, linestyle="dashed", linewidth=1.0,
                label="reference")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


@poi_style(size=FIG_FULL)
def fig_wb2_q1():
    rng = np.random.default_rng(201)
    n = 50
    x = rng.uniform(0, 10, n)
    y = 1.0 + 0.7 * x + rng.normal(0, 1.0, n)
    fig, ax = plt.subplots()
    xline = np.array([0, 10])
    _scatter(ax, x, y, line_x=xline, line_y=xline, ref_y=xline)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("50 points, linear truth", fontsize=11)
    ax.legend(frameon=False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q2():
    rng = np.random.default_rng(202)
    n = 60
    x = np.sort(rng.uniform(0, 12, n))
    y = 0.5 + 0.4 * x - 0.05 * x ** 2 + rng.normal(0, 0.3, n)
    # OLS straight-line fit
    slope, intercept = np.polyfit(x, y, 1)
    fig, ax = plt.subplots()
    _scatter(ax, x, y, line_x=x, line_y=intercept + slope * x)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("60 points, with OLS line through curved truth", fontsize=11)
    ax.legend(frameon=False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q3():
    rng = np.random.default_rng(203)
    n = 80
    x = np.sort(rng.uniform(0, 10, n))
    y = 0.5 + 0.6 * x + rng.normal(0, 0.2 + 0.15 * x, n)
    slope, intercept = np.polyfit(x, y, 1)
    fig, ax = plt.subplots()
    _scatter(ax, x, y, line_x=x, line_y=intercept + slope * x)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("80 points: variance grows with x (heteroskedastic)",
                 fontsize=11)
    ax.legend(frameon=False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q4():
    rng = np.random.default_rng(204)
    n = 50
    x = rng.uniform(0, 10, n)
    y = 0.5 * x + rng.normal(0, 0.7, n)
    # Outlier at high x and substantially below the slope-0.5 line
    x_out = 25.0
    y_out = 12.0
    x_all = np.append(x, x_out)
    y_all = np.append(y, y_out)
    slope_all, int_all = np.polyfit(x_all, y_all, 1)
    slope_no, int_no = np.polyfit(x, y, 1)
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=30, color=INK, alpha=0.6,
               edgecolor="white", linewidth=0.5)
    ax.scatter([x_out], [y_out], s=120, color=RUST,
               edgecolor="white", linewidth=1.5, label="outlier")
    xline = np.array([0, 26])
    ax.plot(xline, int_all + slope_all * xline, color=RUST,
            linewidth=1.6, label=f"OLS with outlier (slope={slope_all:.2f})")
    ax.plot(xline, int_no + slope_no * xline, color=SAGE,
            linewidth=1.6, linestyle="dashed",
            label=f"OLS without outlier (slope={slope_no:.2f})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Single high-leverage outlier shifts the slope", fontsize=11)
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q5():
    rng = np.random.default_rng(205)
    n = 80
    x = rng.normal(0, 1, n)
    y = rng.normal(0, 1, n)
    slope, intercept = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]
    fig, ax = plt.subplots()
    xline = np.array([x.min(), x.max()])
    _scatter(ax, x, y, line_x=xline, line_y=intercept + slope * xline)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"80 independent points: r = {r:+.2f}", fontsize=11)
    ax.legend(frameon=False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q6():
    rng = np.random.default_rng(206)
    # Group A: low x, high y, slope 0.5
    nA = 30
    xA = rng.uniform(0, 4, nA)
    yA = 8 + 0.5 * xA + rng.normal(0, 0.5, nA)
    # Group B: high x, low y, slope 0.5
    nB = 30
    xB = rng.uniform(6, 10, nB)
    yB = 1 + 0.5 * xB + rng.normal(0, 0.5, nB)
    x_all = np.concatenate([xA, xB])
    y_all = np.concatenate([yA, yB])
    slope_pool, int_pool = np.polyfit(x_all, y_all, 1)
    slope_A, int_A = np.polyfit(xA, yA, 1)
    slope_B, int_B = np.polyfit(xB, yB, 1)
    fig, ax = plt.subplots()
    ax.scatter(xA, yA, s=30, color=INK, alpha=0.7,
               edgecolor="white", linewidth=0.5, label="Group A")
    ax.scatter(xB, yB, s=30, color=RUST, alpha=0.7,
               edgecolor="white", linewidth=0.5, label="Group B")
    xline_full = np.array([0, 10])
    ax.plot(xline_full, int_pool + slope_pool * xline_full,
            color=DIM, linewidth=1.8,
            label=f"Pooled OLS (slope={slope_pool:+.2f})")
    ax.plot([0, 4], [int_A, int_A + slope_A * 4],
            color=INK, linewidth=1.4, linestyle="dashed",
            label=f"Group A within (slope={slope_A:+.2f})")
    ax.plot([6, 10], [int_B + slope_B * 6, int_B + slope_B * 10],
            color=RUST, linewidth=1.4, linestyle="dashed",
            label=f"Group B within (slope={slope_B:+.2f})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Simpson's paradox: pooled slope reverses within-group slope",
                 fontsize=11)
    ax.legend(frameon=False, fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q7():
    rng = np.random.default_rng(207)
    n = 40
    x = np.sort(rng.uniform(0, 12, n))
    y_true = 20 + 8 * x + rng.normal(0, 5, n)
    y = np.minimum(y_true, 100)
    slope, intercept = np.polyfit(x, y, 1)
    fig, ax = plt.subplots()
    _scatter(ax, x, y, line_x=x, line_y=intercept + slope * x)
    ax.axhline(100, color=DIM, linestyle="dotted", linewidth=1.0,
               label="ceiling at y=100")
    ax.set_xlabel("x")
    ax.set_ylabel("y (capped at 100)")
    ax.set_title("Ceiling effect: the linear slope underestimates the truth",
                 fontsize=11)
    ax.legend(frameon=False)
    return fig


@poi_style(size=(10, 4.5))
def fig_wb2_q8():
    rng = np.random.default_rng(208)
    n = 60
    x = np.sort(rng.uniform(0, 10, n))
    y_tight = 1.0 + 0.5 * x + rng.normal(0, 0.4, n)
    y_loose = 1.0 + 0.5 * x + rng.normal(0, 1.8, n)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ax, y, title in zip(
        axes,
        [y_tight, y_loose],
        ["Tight residuals  (R² ≈ 0.89)",
         "Loose residuals  (R² ≈ 0.20)"],
    ):
        slope, intercept = np.polyfit(x, y, 1)
        r2 = 1 - np.var(y - (intercept + slope * x)) / np.var(y)
        _scatter(ax, x, y, line_x=x, line_y=intercept + slope * x)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"{title}, slope = {slope:.2f}", fontsize=11)
    plt.tight_layout()
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q9():
    """GDHI vs median house price by English/Welsh local authority district."""
    import pandas as pd

    # Load GDHI data from inequality metrics (344 LADs, no duplicates)
    gdhi = pd.read_parquet('/Volumes/HELFRICH-GD/UK_EconomicData/data/processed/UK_inequality_metrics_LAD.parquet')
    gdhi = gdhi.drop(columns=['geometry'], errors='ignore')
    gdhi = gdhi.dropna(subset=['GDHI_2016'])[['LAD23CD', 'GDHI_2016']].drop_duplicates('LAD23CD')

    # Load median house price data (year ending Sep 2016, col index 23)
    aff_raw = pd.read_parquet('/Volumes/HELFRICH-GD/UK_EconomicData/data/raw/Affordability_LAD.parquet')
    col_headers = aff_raw.iloc[0].tolist()
    aff_raw.columns = col_headers
    aff = aff_raw.iloc[1:].copy()
    aff = aff.rename(columns={
        'Local authority code': 'LAD23CD',
        'Year ending Sep 2016': 'median_house_price_2016',
    })
    aff = aff[['LAD23CD', 'median_house_price_2016']].copy()
    aff['median_house_price_2016'] = pd.to_numeric(aff['median_house_price_2016'], errors='coerce')
    # Keep only real LAD codes (England/Wales LADs)
    aff = aff[aff['LAD23CD'].str.match(r'^[EW][0-9]', na=False)]
    aff = aff.dropna(subset=['median_house_price_2016']).drop_duplicates('LAD23CD')

    df = gdhi.merge(aff, on='LAD23CD', how='inner')
    df = df.dropna(subset=['GDHI_2016', 'median_house_price_2016'])

    x = df['GDHI_2016'].values
    y = df['median_house_price_2016'].values / 1000   # convert to £ thousands

    slope, intercept = np.polyfit(x, y, 1)
    xline = np.array([x.min(), x.max()])

    # Identify London LADs (roughly: median house price > £500k)
    is_london = y > 500

    n = len(df)
    fig, ax = plt.subplots()
    ax.scatter(x[~is_london], y[~is_london], s=28, color=INK, alpha=0.6,
               edgecolor='white', linewidth=0.5, label='Other LADs')
    ax.scatter(x[is_london], y[is_london], s=60, color=RUST, alpha=0.8,
               edgecolor='white', linewidth=0.8, label='London boroughs')
    ax.plot(xline, intercept + slope * xline, color=GOLD, linewidth=1.8,
            label=f'OLS slope = {slope:.2f} (£k per £ GDHI)')
    ax.set_xlabel('gross disposable household income per head, 2016 (£)')
    ax.set_ylabel('median house price (£ thousands)')
    ax.set_title(f'Do richer areas have higher house prices? {n} UK local authorities',
                 fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_wb2_q10():
    """Income deprivation vs health deprivation across English LSOAs (IMD 2019)."""
    import pandas as pd
    rng = np.random.default_rng(1002)
    df = pd.read_parquet('/Volumes/HELFRICH-GD/UK_EconomicData/data/raw/IMD_2019_England.parquet')
    # Sample 2000 LSOAs for speed
    df = df.sample(n=2000, random_state=1002)
    x = df['Income Score (rate)'].values
    y = df['Health Deprivation and Disability Score'].values
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    slope, intercept = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=8, color=INK, alpha=0.25, edgecolor='none')
    xline = np.array([x.min(), x.max()])
    ax.plot(xline, intercept + slope * xline, color=RUST, linewidth=2.0,
            label=f'OLS fit, r = {r:.2f}')
    ax.set_xlabel('income deprivation score (rate)')
    ax.set_ylabel('health deprivation score')
    ax.set_title('Income and health deprivation by LSOA, England 2019\n(sample of 2,000 areas)',
                 fontsize=11)
    ax.legend(frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig
