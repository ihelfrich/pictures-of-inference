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
    """Apply book-wide matplotlib defaults. Called by @poi_style.

    Font policy: stick with matplotlib's reliable defaults (DejaVu Sans
    for sans, DejaVu Serif for serif). The HTML book's typography is
    handled by Quarto/CSS; figures don't need to share the typeface
    because they live in their own visual frame. Avoiding system
    Palatino also dodges the 'Zapf NOT subset' warnings on macOS.
    """
    matplotlib.rcParams.update({
        # PDF compatibility
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",  # keep text as text in SVG output

        # Typography: clean sans-serif everywhere, matplotlib defaults.
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial",
                            "sans-serif"],
        "font.size": 11.5,
        "axes.titlesize": 13,
        "axes.titleweight": "regular",
        "axes.titlepad": 12,
        "axes.labelsize": 11.5,
        "axes.labelweight": "regular",
        "axes.labelpad": 6,
        "xtick.labelsize": 10.5,
        "ytick.labelsize": 10.5,
        "legend.fontsize": 10.5,
        "legend.frameon": False,
        "figure.titlesize": 14,

        # Math: use matplotlib's mathtext, not LaTeX (faster, portable).
        "mathtext.fontset": "dejavusans",
        "mathtext.default": "regular",

        # Lines and markers (heavier so figures read on big screens)
        "lines.linewidth": 1.9,
        "lines.markersize": 5,
        "patch.linewidth": 0.8,

        # Spines: minimal, slightly heavier so they don't disappear
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.9,
        "axes.edgecolor": "#444444",

        # Ticks: outward, light
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.color": "#444444",
        "ytick.color": "#444444",

        # Grid: subtle, not dominant
        "axes.grid": True,
        "axes.grid.axis": "both",
        "grid.alpha": 0.22,
        "grid.linewidth": 0.6,
        "grid.color": "#888888",

        # Color cycle defaults to the POI palette
        "axes.prop_cycle": matplotlib.cycler(color=[
            INK, RUST, SAGE, GOLD, VIOLET, TEAL, DIM
        ]),

        # Saving: high DPI for crisp rendering
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.18,
        "savefig.transparent": False,
        "savefig.facecolor": "white",
        "figure.dpi": 150,
        "figure.facecolor": "white",
        "figure.edgecolor": "white",
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
            stem = name or func.__name__
            # Save as PNG (for HTML — renders inline, no PDF viewer)
            # AND PDF (for print/LaTeX).
            fig.savefig(outdir / f"{stem}.png", dpi=300)
            fig.savefig(outdir / f"{stem}.pdf")
            print(f"  saved {stem}.png + {stem}.pdf")
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
