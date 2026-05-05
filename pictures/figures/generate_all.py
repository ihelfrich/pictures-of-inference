#!/usr/bin/env python3
"""
Generate all figures for the book.

Usage:
    python pictures/figures/generate_all.py             # all chapters
    python pictures/figures/generate_all.py --ch 01     # specific chapter
    python pictures/figures/generate_all.py --list      # list available
"""

from __future__ import annotations
import argparse
import importlib
import sys
from pathlib import Path

# Make the lib importable
HERE = Path(__file__).resolve().parent
LIB = HERE.parent / "lib"
sys.path.insert(0, str(LIB))


def discover_chapters() -> list[str]:
    """Find all chXX.py and wbXX.py modules in this directory."""
    return sorted(
        f.stem for f in HERE.iterdir()
        if f.is_file() and f.suffix == ".py"
        and f.stem != "generate_all"
        and (f.stem.startswith("ch") or f.stem.startswith("wb"))
    )


def run_chapter(slug: str) -> None:
    """Import a chapter module and run all its figure functions."""
    print(f"\n=== {slug} ===")
    module = importlib.import_module(slug)
    fig_funcs = [
        getattr(module, name) for name in dir(module)
        if name.startswith("fig_") and callable(getattr(module, name))
    ]
    if not fig_funcs:
        print(f"  (no figure functions found in {slug})")
        return
    for func in fig_funcs:
        try:
            func()
        except FileNotFoundError as e:
            # Local-only data (e.g. external drive with UK datasets).
            # Pre-generated PNGs are committed to the repo; skip silently on CI.
            print(f"  SKIPPED {func.__name__}: data not available ({e})")
        except Exception as e:
            print(f"  ERROR in {func.__name__}: {e}")
            raise


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ch", help="Run only this chapter (e.g., 01)")
    p.add_argument("--list", action="store_true",
                   help="List available chapters and exit")
    args = p.parse_args()

    chapters = discover_chapters()

    if args.list:
        for c in chapters:
            print(c)
        return

    if args.ch:
        slug = f"ch{args.ch.zfill(2)}"
        if slug not in chapters:
            print(f"Chapter {slug!r} not found. Available: {chapters}")
            sys.exit(1)
        run_chapter(slug)
    else:
        for slug in chapters:
            run_chapter(slug)

    print("\nAll figures generated.")


if __name__ == "__main__":
    main()
