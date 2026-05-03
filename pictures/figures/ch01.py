"""
Figures for Chapter 1: Numbers on the Page.

This is a placeholder demonstrating the pattern. Real figures land here
when the chapter is drafted.
"""

from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, DIM,
    FIG_SINGLE, FIG_FULL,
)
import matplotlib.pyplot as plt
import numpy as np


@poi_style
def fig_data_rectangle():
    """
    Demonstrates the basic shape of a dataset: rows are units, columns
    are variables.
    """
    fig, ax = plt.subplots()

    # Draw a stylized data rectangle
    rows, cols = 6, 5
    for i in range(rows + 1):
        ax.axhline(i, color=DIM, lw=0.8, alpha=0.4)
    for j in range(cols + 1):
        ax.axvline(j, color=DIM, lw=0.8, alpha=0.4)

    # Highlight a row
    ax.axhspan(2, 3, alpha=0.15, color=INK)
    ax.text(-0.5, 2.5, "one row =\none unit",
            ha="right", va="center", fontsize=9, color=INK)

    # Highlight a column
    ax.axvspan(2, 3, alpha=0.15, color=RUST)
    ax.text(2.5, rows + 0.5, "one column =\none variable",
            ha="center", va="bottom", fontsize=9, color=RUST)

    ax.set_xlim(-2, cols + 1)
    ax.set_ylim(-0.5, rows + 1.5)
    ax.set_aspect("equal")
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    return fig


@poi_style(size=FIG_SINGLE)
def fig_variable_types():
    """
    A small visual taxonomy of variable types.
    """
    fig, ax = plt.subplots()

    types = ["Quantitative", "Ordinal", "Categorical"]
    colors = [INK, GOLD, SAGE]
    examples = ["GPA, age, income", "ranks, Likert", "country, sex"]

    for i, (t, c, ex) in enumerate(zip(types, colors, examples)):
        ax.barh(i, 1, color=c, alpha=0.7)
        ax.text(0.05, i, t, va="center", fontsize=11,
                color="white", fontweight="bold")
        ax.text(1.05, i, ex, va="center", fontsize=9, color=DIM)

    ax.set_xlim(0, 2.5)
    ax.set_ylim(-0.5, len(types) - 0.5)
    ax.invert_yaxis()
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    return fig
