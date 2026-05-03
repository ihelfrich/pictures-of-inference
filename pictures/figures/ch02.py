"""
Figures for Chapter 2: Probability as area.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_SINGLE, FIG_FULL, FIG_SQUARE,
)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


@poi_style(size=FIG_FULL)
def fig_sample_space():
    """All 36 outcomes of rolling two dice; cells colored by sum."""
    fig, ax = plt.subplots()

    # Build the grid: cell (i, j) has sum (i+1)+(j+1)
    # Color intensity tracks how common that sum is (1..6 cells per sum).
    sums = np.add.outer(np.arange(1, 7), np.arange(1, 7))
    counts = 6 - np.abs(7 - sums)  # 1 for sums 2 or 12, 6 for sum 7

    # Custom blue ramp tied to INK
    cmap = LinearSegmentedColormap.from_list(
        "ink_ramp", ["#e6eef5", "#a3bdd4", "#5a85b3", "#2c628f", "#1a4f7a"]
    )

    for i in range(6):
        for j in range(6):
            intensity = (counts[i, j] - 1) / 5.0  # 0 to 1
            color = cmap(0.2 + 0.7 * intensity)
            ax.add_patch(plt.Rectangle((j, i), 0.96, 0.96,
                                       facecolor=color, edgecolor="white",
                                       linewidth=2))
            text_color = "white" if intensity > 0.5 else INK
            ax.text(j + 0.48, i + 0.48, str(int(sums[i, j])),
                    ha="center", va="center", fontsize=11,
                    color=text_color, fontweight="bold")

    ax.set_xlim(-0.05, 6.0)
    ax.set_ylim(-0.05, 6.0)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(6) + 0.48)
    ax.set_xticklabels(range(1, 7))
    ax.set_yticks(np.arange(6) + 0.48)
    ax.set_yticklabels(range(1, 7))
    ax.set_xlabel("Die 1")
    ax.set_ylabel("Die 2")
    ax.invert_yaxis()
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Sample space: 36 outcomes of two fair dice",
                 fontsize=11, pad=10)
    return fig


@poi_style(size=FIG_FULL)
def fig_events_overlap():
    """Two overlapping events inside a rectangular sample space."""
    fig, ax = plt.subplots()

    # Sample space rectangle
    ax.add_patch(plt.Rectangle((0, 0), 10, 6, fill=False,
                               edgecolor=DIM, linewidth=1.5))

    # Two overlapping circles
    circ_a = plt.Circle((3.7, 3), 2.0, alpha=0.55,
                        facecolor=INK, edgecolor=INK, linewidth=1.2)
    circ_b = plt.Circle((6.3, 3), 2.0, alpha=0.55,
                        facecolor=RUST, edgecolor=RUST, linewidth=1.2)
    ax.add_patch(circ_a)
    ax.add_patch(circ_b)

    ax.text(2.6, 3, "A", ha="center", va="center",
            fontsize=22, color="white", fontweight="bold")
    ax.text(7.4, 3, "B", ha="center", va="center",
            fontsize=22, color="white", fontweight="bold")
    ax.text(5.0, 3, r"$A \cap B$", ha="center", va="center",
            fontsize=12, color="white", fontweight="bold")
    ax.text(0.3, 5.6, "Sample space  S",
            ha="left", va="top", fontsize=10, color=DIM, style="italic")

    # Caption-ish labels at the bottom
    ax.text(2.6, 0.4, "13 hearts",
            ha="center", va="center", fontsize=9, color=INK)
    ax.text(7.4, 0.4, "12 face cards",
            ha="center", va="center", fontsize=9, color=RUST)
    ax.text(5.0, 0.4, "3 hearts that\nare face cards",
            ha="center", va="center", fontsize=8, color="#5a3022")

    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(-0.3, 6.3)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    return fig


@poi_style(size=FIG_FULL)
def fig_conditional_zoom():
    """Two panels: left full deck (face cards highlighted), right hearts only."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5))

    suits = ["S", "H", "D", "C"]  # Spades, Hearts, Diamonds, Clubs
    suit_color = {"S": INK, "C": INK, "H": RUST, "D": RUST}
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    is_face = lambda r: r in {"J", "Q", "K"}

    # Panel 1: full deck (4 suits × 13 cards), top to bottom: S, H, D, C
    for i, suit in enumerate(suits):
        for j, rank in enumerate(ranks):
            highlight = is_face(rank)
            face = GOLD if highlight else "white"
            edge = suit_color[suit]
            ax1.add_patch(plt.Rectangle((j, 3 - i), 0.92, 0.92,
                                        facecolor=face, edgecolor=edge,
                                        linewidth=0.7))
            ax1.text(j + 0.46, 3 - i + 0.46, f"{rank}{suit}",
                     ha="center", va="center", fontsize=7, color=edge)
    ax1.set_xlim(-0.2, 13.2)
    ax1.set_ylim(-0.3, 4.3)
    ax1.set_aspect("equal")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title("Full deck of 52 cards\n12 face cards (gold)",
                  fontsize=10)
    for s in ax1.spines.values():
        s.set_visible(False)

    # Panel 2: just hearts, single row
    for j, rank in enumerate(ranks):
        highlight = is_face(rank)
        face = GOLD if highlight else "white"
        ax2.add_patch(plt.Rectangle((j, 0.5), 0.92, 0.92,
                                    facecolor=face, edgecolor=RUST,
                                    linewidth=1))
        ax2.text(j + 0.46, 0.96, f"{rank}H",
                 ha="center", va="center", fontsize=9, color=RUST)
    ax2.set_xlim(-0.2, 13.2)
    ax2.set_ylim(-0.3, 2.5)
    ax2.set_aspect("equal")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_title("Conditioned on hearts (13 cards)\n3 are face cards",
                  fontsize=10)
    for s in ax2.spines.values():
        s.set_visible(False)
    return fig


@poi_style(size=(7.0, 7.5))
def fig_bayes_grid():
    """The disease-test grid: 10000 people, four colored regions."""
    fig, ax = plt.subplots()

    n_sick_pos = 95
    n_sick_neg = 5
    n_well_pos = 495
    n_well_neg = 9405

    # Colors
    DARK_RED = (0.55, 0.13, 0.20)
    PALE_RED = (0.93, 0.74, 0.74)
    RUST_RGB = (0.722, 0.36, 0.22)
    GRAY = (0.85, 0.85, 0.85)

    flat = (
        [DARK_RED] * n_sick_pos
        + [PALE_RED] * n_sick_neg
        + [RUST_RGB] * n_well_pos
        + [GRAY] * n_well_neg
    )
    grid = np.zeros((100, 100, 3))
    for idx, color in enumerate(flat):
        r = idx // 100
        c = idx % 100
        grid[r, c] = color

    ax.imshow(grid, origin="upper", interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("10,000 people: disease status × test result\n"
                 "(read row by row, top-left to bottom-right)",
                 fontsize=11, pad=12)

    # Annotation arrows
    ax.annotate("100 sick\n(top row of grid)", xy=(50, 0.5), xytext=(110, 5),
                arrowprops=dict(arrowstyle="-", color=DARK_RED, lw=1.0),
                fontsize=9, color=DARK_RED, ha="left", va="center")
    ax.annotate("9,900 well\n(rest of grid)", xy=(50, 50), xytext=(110, 50),
                arrowprops=dict(arrowstyle="-", color=DIM, lw=1.0),
                fontsize=9, color=DIM, ha="left", va="center")

    # Legend below
    handles = [
        mpatches.Patch(facecolor=DARK_RED, label="Sick & test +  (95 true positives)"),
        mpatches.Patch(facecolor=PALE_RED, label="Sick & test −  (5 false negatives)"),
        mpatches.Patch(facecolor=RUST_RGB, label="Well & test +  (495 false positives)"),
        mpatches.Patch(facecolor=GRAY,    label="Well & test −  (9,405 true negatives)"),
    ]
    ax.legend(handles=handles, loc="upper center",
              bbox_to_anchor=(0.5, -0.04),
              ncol=2, fontsize=9, frameon=False)

    # Make room for legend and right-side annotations
    ax.set_xlim(-2, 175)
    ax.set_ylim(102, -5)
    ax.set_aspect("equal")
    return fig
