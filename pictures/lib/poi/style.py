"""
poi.style
=========

Centralized styling for all figures in Pictures of Inference.
Import from this module; do not hard-code colors or fonts elsewhere.

Usage
-----

    from poi.style import poi_style, INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL
    import matplotlib.pyplot as plt

    @poi_style
    def fig_my_figure():
        fig, ax = plt.subplots()
        ax.plot(x, y, color=INK)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        return fig

The @poi_style decorator handles fonts, sizing, saving, and output paths.
"""

from __future__ import annotations
from pathlib import Path
import functools
import matplotlib
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Palette (semantic colors)
# ------------------------------------------------------------

INK    = "#1a4f7a"   # primary, default, the main story
RUST   = "#b85c38"   # treatment, contrast, the alternative perspective
SAGE   = "#5a7247"   # control, comparison, the baseline
GOLD   = "#b8941e"   # highlighted, derived, the synthesized quantity
VIOLET = "#6a5acd"   # uncertain, predicted, the model's guess
DIM    = "#8a8a8a"   # background, de-emphasized, support
TEAL   = "#3a8a99"   # alternative or secondary contrast

PALETTE = {
    "INK": INK,
    "RUST": RUST,
    "SAGE": SAGE,
    "GOLD": GOLD,
    "VIOLET": VIOLET,
    "DIM": DIM,
    "TEAL": TEAL,
}

# Sequential palette (use for ordered/continuous categories)
SEQ_BLUES = ["#d6e4f0", "#a8c5e0", "#6c9bc7", "#3a73a8", "#1a4f7a"]
SEQ_WARM  = ["#f5dccb", "#e8b395", "#d68a64", "#b85c38", "#7a3a1f"]

# Diverging palette (use for signed quantities centered at zero)
DIV_BLUE_RUST = [INK, "#6c9bc7", "#d6e4f0", "#f5f5f5",
                 "#f5dccb", "#d68a64", RUST]


# ------------------------------------------------------------
# Sizes (in inches)
# ------------------------------------------------------------

FIG_SINGLE = (5.5, 3.6)     # single column (in margin or half-width)
FIG_FULL   = (9.0, 5.5)     # full text body, the default
FIG_SPREAD = (12.0, 6.5)    # extra-wide, page-column or screen-inset
FIG_TALL   = (6.0, 7.5)     # vertical
FIG_SQUARE = (7.0, 7.0)     # square


# ------------------------------------------------------------
# Output paths
# ------------------------------------------------------------

# Resolve at import time relative to repo root
_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[3]   # poi/pictures/lib/poi/style.py -> poi/
FIG_OUTPUT = REPO_ROOT / "pictures" / "figures" / "output"
FIG_OUTPUT.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Matplotlib defaults
# ------------------------------------------------------------

def apply_defaults() -> None:
    """Apply book-wide matplotlib defaults. Called by @poi_style."""
    matplotlib.rcParams.update({
        # PDF compatibility
        "pdf.fonttype": 42,
        "ps.fonttype": 42,

        # Typography
        "font.family": "serif",
        "font.serif": ["Palatino", "Palatino Linotype", "DejaVu Serif",
                       "serif"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 12,

        # Lines and markers
        "lines.linewidth": 1.6,
        "lines.markersize": 4,
        "patch.linewidth": 0.7,

        # Spines
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.7,

        # Grid
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.5,

        # Color cycle defaults to the palette
        "axes.prop_cycle": matplotlib.cycler(color=[
            INK, RUST, SAGE, GOLD, VIOLET, TEAL, DIM
        ]),

        # Saving
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.15,
        "savefig.transparent": False,
        "figure.dpi": 110,

        # Title / label sizes scaled up for the new larger default
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 13,
    })


# ------------------------------------------------------------
# The decorator
# ------------------------------------------------------------

def poi_style(name: str | None = None,
              size: tuple[float, float] = FIG_FULL,
              save: bool = True,
              output_dir: Path | None = None):
    """
    Decorator that handles styling, sizing, and saving for figure functions.

    The decorated function should:
      - Accept no arguments (or default-only).
      - Return a matplotlib Figure.

    Use as either:
        @poi_style                  # uses function name, default size
        def fig_xxx(): ...

        @poi_style(size=FIG_SINGLE)   # custom size
        def fig_xxx(): ...

    The figure is saved as <name>.pdf in pictures/figures/output/.
    """
    # Allow @poi_style without parentheses
    if callable(name):
        func = name
        return _wrap_figure(func, name=None, size=FIG_FULL,
                            save=True, output_dir=None)

    def decorator(func):
        return _wrap_figure(func, name=name, size=size,
                            save=save, output_dir=output_dir)

    return decorator


def _wrap_figure(func, name, size, save, output_dir):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        apply_defaults()
        fig = func(*args, **kwargs)
        if fig is None:
            raise RuntimeError(
                f"Figure function {func.__name__!r} returned None. "
                "It must return a matplotlib Figure object."
            )
        if size is not None:
            fig.set_size_inches(*size)
        fig.tight_layout()
        if save:
            outdir = Path(output_dir) if output_dir else FIG_OUTPUT
            outdir.mkdir(parents=True, exist_ok=True)
            fname = (name or func.__name__) + ".pdf"
            fig.savefig(outdir / fname)
            print(f"  saved {fname}")
        return fig
    return wrapper


# ------------------------------------------------------------
# Convenience helpers
# ------------------------------------------------------------

def clean_axes(ax, x=True, y=True):
    """Remove top and right spines, clean up tick directions."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if x:
        ax.tick_params(axis="x", direction="out", length=4)
    if y:
        ax.tick_params(axis="y", direction="out", length=4)
    return ax


def annotate_value(ax, x, y, text, **kwargs):
    """Annotate a point with consistent styling."""
    defaults = {
        "fontsize": 9,
        "ha": "left",
        "va": "bottom",
        "xytext": (4, 4),
        "textcoords": "offset points",
    }
    defaults.update(kwargs)
    ax.annotate(text, xy=(x, y), **defaults)
