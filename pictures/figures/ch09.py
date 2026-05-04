"""
Figures for Chapter 9: Reading equations.

Anatomy diagrams: each equation rendered large with annotated parts.
"""
from poi import (
    poi_style,
    INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL,
    FIG_FULL,
)
import matplotlib.pyplot as plt


@poi_style(size=(9, 5))
def fig_eq_expectation():
    """E[Y | X = x] with annotations."""
    fig, ax = plt.subplots()

    # Big equation, math via matplotlib's mathtext
    ax.text(0.50, 0.65, r"$\mathbb{E}\,[\,Y\,\mid\,X = x\,]$",
            fontsize=58, ha="center", va="center", color=INK)

    # Annotations: (anchor_x, anchor_y) -> (text_x, text_y)
    annots = [
        (0.32, 0.72, 0.16, 0.92, "expectation\noperator", INK),
        (0.42, 0.62, 0.30, 0.20, "random variable\nof interest", RUST),
        (0.50, 0.72, 0.50, 0.95, "given\n(vertical bar)", SAGE),
        (0.66, 0.62, 0.78, 0.20, "the value X took\n(lowercase = specific value)", GOLD),
    ]
    for ax_anc, ay_anc, tx, ty, label, color in annots:
        ax.annotate(
            label,
            xy=(ax_anc, ay_anc), xytext=(tx, ty),
            arrowprops=dict(arrowstyle="-", color=color, lw=1.0,
                            connectionstyle="arc3,rad=0.0"),
            fontsize=10, color=color, ha="center", va="center",
        )

    ax.text(0.5, 0.05,
            r"read aloud:  $the\ expected\ value\ of\ Y\ given\ that\ X\ equals\ x$",
            fontsize=11, ha="center", va="center", color=DIM, style="italic")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig


@poi_style(size=(11, 5))
def fig_eq_ols():
    """OLS estimator in matrix form, annotated."""
    fig, ax = plt.subplots()

    ax.text(0.50, 0.62,
            r"$\hat{\beta}\;=\;(\mathbf{X}^{\!\top}\mathbf{X})^{-1}\,\mathbf{X}^{\!\top}\mathbf{y}$",
            fontsize=54, ha="center", va="center", color=INK)

    annots = [
        (0.33, 0.68, 0.10, 0.95, "estimator\n(hat = estimate of true β)", INK),
        (0.45, 0.66, 0.30, 0.18, "Gram matrix:\nk × k square", RUST),
        (0.55, 0.68, 0.55, 0.95, "inverse\n(undoes the matrix)", SAGE),
        (0.66, 0.66, 0.70, 0.18, "X-transpose times y:\nk × 1 vector", GOLD),
        (0.74, 0.66, 0.93, 0.95, "outcome vector\n(length n)", VIOLET),
    ]
    for ax_anc, ay_anc, tx, ty, label, color in annots:
        ax.annotate(
            label,
            xy=(ax_anc, ay_anc), xytext=(tx, ty),
            arrowprops=dict(arrowstyle="-", color=color, lw=1.0),
            fontsize=9.5, color=color, ha="center", va="center",
        )

    ax.text(0.5, 0.05,
            r"read aloud:  $beta\!\!-\!\!hat\ equals\ X\!-\!transpose\!-\!X\ inverse,\ times\ X\!-\!transpose\!-\!y$",
            fontsize=10.5, ha="center", va="center", color=DIM, style="italic")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig


@poi_style(size=(9, 5.5))
def fig_eq_bayes():
    """Bayes' theorem with the four named pieces."""
    fig, ax = plt.subplots()

    ax.text(0.50, 0.60,
            r"$P(A\mid B)\;=\;\dfrac{P(B\mid A)\,P(A)}{P(B)}$",
            fontsize=44, ha="center", va="center", color=INK)

    annots = [
        (0.27, 0.60, 0.10, 0.92, "POSTERIOR\nwhat we want", INK),
        (0.55, 0.74, 0.55, 0.94, "LIKELIHOOD\nhow evidence behaves\nif A is true", RUST),
        (0.73, 0.74, 0.93, 0.94, "PRIOR\nwhat we believed before", GOLD),
        (0.62, 0.46, 0.62, 0.18, "MARGINAL\ntotal probability\nof the evidence", SAGE),
    ]
    for ax_anc, ay_anc, tx, ty, label, color in annots:
        ax.annotate(
            label,
            xy=(ax_anc, ay_anc), xytext=(tx, ty),
            arrowprops=dict(arrowstyle="-", color=color, lw=1.0),
            fontsize=9.5, color=color, ha="center", va="center",
            fontweight="bold",
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig
