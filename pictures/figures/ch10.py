"""
Figures for Chapter 10: Reading tables.

Mock journal-style tables rendered as matplotlib figures so they
travel with the chapter and can be styled consistently.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_FULL,
)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def _render_journal_table(ax, headers, rows, col_widths=None, title=None,
                          notes=None, footers=None, hsep_after=None):
    """
    Draw a clean book-style table with three horizontal rules.
    headers:  list of strings (top row)
    rows:     list of lists (each row of cells)
    hsep_after: list of row indices after which to draw a thin rule
    footers:  list of lists (rendered without separating rule above the
              first; included with same column structure)
    """
    n_cols = len(headers)
    if col_widths is None:
        col_widths = [1.0] + [0.7] * (n_cols - 1)
    total = sum(col_widths)
    edges = [0.0]
    for w in col_widths:
        edges.append(edges[-1] + w / total)

    cell_h = 0.055
    n_rows = len(rows)
    n_footers = len(footers) if footers else 0

    # Geometry: title at the top, headers, rules, body, then footers, notes.
    top = 0.95
    if title:
        ax.text(0.5, top, title, ha="center", va="bottom",
                fontsize=11, color=INK, fontweight="bold")
        top -= 0.06

    # Top rule
    rule_y = top
    ax.plot([0, 1], [rule_y, rule_y], color=INK, lw=1.4)
    rule_y -= 0.012

    # Headers
    for c, header in enumerate(headers):
        cx = (edges[c] + edges[c + 1]) / 2
        align_first = "left" if c == 0 else "center"
        ax.text(cx if c > 0 else edges[0] + 0.005,
                rule_y - cell_h / 2, header,
                ha=align_first, va="center",
                fontsize=10, color=INK, fontweight="bold")
    rule_y -= cell_h
    ax.plot([0, 1], [rule_y, rule_y], color=INK, lw=0.8)

    # Body rows
    for r, row in enumerate(rows):
        rule_y -= 0.005
        for c, val in enumerate(row):
            align_first = "left" if c == 0 else "center"
            cx = edges[c] + 0.005 if c == 0 else (edges[c] + edges[c + 1]) / 2
            # Style: stars dimmer
            color = INK if c == 0 else (RUST if "*" in str(val) else INK)
            ax.text(cx, rule_y - cell_h / 2, val,
                    ha=align_first, va="center",
                    fontsize=10, color=color,
                    family=("serif" if c == 0 else "monospace"))
        rule_y -= cell_h
        if hsep_after and r in hsep_after:
            ax.plot([0, 1], [rule_y, rule_y], color=DIM, lw=0.4)
            rule_y -= 0.005

    # Footer rule
    ax.plot([0, 1], [rule_y, rule_y], color=DIM, lw=0.4)

    # Footer rows (e.g. N, R^2, FE)
    if footers:
        for row in footers:
            rule_y -= 0.005
            for c, val in enumerate(row):
                align_first = "left" if c == 0 else "center"
                cx = edges[c] + 0.005 if c == 0 else (edges[c] + edges[c + 1]) / 2
                ax.text(cx, rule_y - cell_h / 2, val,
                        ha=align_first, va="center",
                        fontsize=10, color=INK,
                        family=("serif" if c == 0 else "monospace"))
            rule_y -= cell_h

    # Bottom rule
    ax.plot([0, 1], [rule_y, rule_y], color=INK, lw=1.4)

    # Notes
    if notes:
        rule_y -= 0.025
        ax.text(0, rule_y, notes,
                ha="left", va="top",
                fontsize=8.5, color=DIM, style="italic")

    ax.set_xlim(0, 1)
    ax.set_ylim(rule_y - 0.05, 1)
    ax.axis("off")


@poi_style(size=(9.5, 6.5))
def fig_regression_table():
    """A typical regression table with three specifications."""
    fig, ax = plt.subplots()

    headers = ["", "(1)\nbase OLS", "(2)\n+ language", "(3)\n+ FE"]
    rows = [
        ["log GDP exporter",  "0.92***",   "0.95***",   "0.94***"],
        ["",                  "(0.08)",    "(0.07)",    "(0.07)"],
        ["log GDP importer",  "0.81***",   "0.85***",   "0.86***"],
        ["",                  "(0.09)",    "(0.08)",    "(0.08)"],
        ["log distance",     "−0.78***",  "−0.85***",  "−0.83***"],
        ["",                  "(0.11)",    "(0.10)",    "(0.10)"],
        ["common language",   "",          "0.40**",    "0.42**"],
        ["",                  "",          "(0.13)",    "(0.13)"],
        ["constant",         "−2.10",     "−3.60***",  "(absorbed)"],
        ["",                  "(1.20)",    "(0.45)",    ""],
    ]
    footers = [
        ["country-pair FE",  "No",        "No",        "Yes"],
        ["observations",     "300",       "300",       "300"],
        ["R-squared",        "0.78",      "0.81",      "0.94"],
    ]
    _render_journal_table(
        ax, headers, rows,
        col_widths=[1.6, 0.85, 0.85, 0.85],
        title="Table 10.1.  Regression of log bilateral exports on gravity covariates",
        hsep_after=[1, 3, 5, 7],
        notes=("Standard errors clustered at the country-pair level in parentheses. "
               "* p < 0.10, ** p < 0.05, *** p < 0.01.  Synthetic data "
               "(see data/trade/process.py); coefficients are illustrative."),
        footers=footers,
    )

    return fig


@poi_style(size=(9, 5.5))
def fig_summary_table():
    """Summary statistics table."""
    fig, ax = plt.subplots()

    headers = ["variable", "N", "mean", "sd", "min", "p25", "p50", "p75", "max"]
    rows = [
        ["exports (USD M)",        "300", "37,128",    "29,406",  "1,212", "12,892", "29,517",  "53,040",  "163,910"],
        ["GDP exporter (USD T)",   "300", "9.81",      "8.84",    "1.07",  "2.83",   "5.69",    "17.79",   "27.36"],
        ["GDP importer (USD T)",   "300", "9.81",      "8.84",    "1.07",  "2.83",   "5.69",    "17.79",   "27.36"],
        ["distance (km)",          "300", "8,892",     "1,896",   "6,979", "7,850",  "9,997",   "10,534",  "11,587"],
        ["common language (0/1)",  "300", "0.13",      "0.34",    "0",     "0",      "0",       "0",       "1"],
        ["common border (0/1)",    "300", "0.00",      "0.00",    "0",     "0",      "0",       "0",       "0"],
    ]
    _render_journal_table(
        ax, headers, rows,
        col_widths=[1.8, 0.5, 0.85, 0.8, 0.7, 0.75, 0.85, 0.85, 0.95],
        title="Table 10.2.  Summary statistics, bilateral trade panel (2014-2023)",
        notes=("Unit of analysis: country-pair-year (six countries, ten years, "
               "all ordered pairs).  Synthetic placeholder data.  "
               "GDP at current prices, USD trillions."),
    )

    return fig


@poi_style(size=(9, 5.5))
def fig_balance_table():
    """Balance table for a hypothetical RCT."""
    fig, ax = plt.subplots()

    headers = ["covariate", "treatment\nmean", "control\nmean", "difference", "p-value"]
    rows = [
        ["age (years)",                "39.4",  "39.7",  "−0.3",   "0.62"],
        ["female (0/1)",               "0.51",  "0.50",  "0.01",   "0.78"],
        ["years of schooling",         "12.8",  "12.6",  "0.2",    "0.41"],
        ["household income (USD K)",   "48.2",  "47.9",  "0.3",    "0.83"],
        ["urban (0/1)",                "0.62",  "0.60",  "0.02",   "0.51"],
        ["pre-treatment outcome",      "67.1",  "66.8",  "0.3",    "0.74"],
        ["computer at home (0/1)",     "0.85",  "0.83",  "0.02",   "0.46"],
        ["health-insurance (0/1)",     "0.72",  "0.74",  "−0.02",  "0.38"],
    ]
    footers = [
        ["observations", "1,034", "1,029", "", ""],
    ]
    _render_journal_table(
        ax, headers, rows,
        col_widths=[2.0, 0.9, 0.9, 0.9, 0.7],
        title="Table 10.3.  Pre-treatment balance, hypothetical RCT (n = 2,063)",
        notes=("Means by assigned condition. Differences and p-values from a "
               "two-sided t-test with no adjustment for multiple comparisons. "
               "Hypothetical data; balanced design assumed."),
        footers=footers,
    )

    return fig
