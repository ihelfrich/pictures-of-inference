#!/usr/bin/env python3
"""
Build a single chapter as a standalone PDF.

Usage:
    python tools/build_chapter.py 01
    python tools/build_chapter.py 12

Looks for prose/partN/<NN>-*.tex in any part directory.
"""

from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
PROSE = REPO / "prose"
BUILD = REPO / "build" / "pdf"


def find_chapter(num: str) -> Path | None:
    """Find chapter file by number across all part directories."""
    num_padded = num.zfill(2)
    for part_dir in sorted(PROSE.glob("part*")):
        for f in part_dir.glob(f"{num_padded}-*.tex"):
            return f
    return None


def build(chapter_path: Path) -> None:
    BUILD.mkdir(parents=True, exist_ok=True)

    # Build a tiny driver wrapping just this chapter
    driver = BUILD / f"chapter_{chapter_path.stem}.tex"
    chapter_relpath = chapter_path.relative_to(PROSE).with_suffix("")

    driver.write_text(rf"""
\input{{{PROSE}/preamble}}
\begin{{document}}
\input{{{PROSE}/{chapter_relpath}}}
\end{{document}}
""")

    print(f"Building {chapter_path.name}...")
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={BUILD}", driver.name],
            cwd=BUILD, capture_output=True, text=True
        )
        if result.returncode != 0:
            print("LaTeX errors:")
            print(result.stdout[-2000:])
            sys.exit(1)

    pdf_out = BUILD / f"chapter_{chapter_path.stem}.pdf"
    print(f"  -> {pdf_out}")


def main():
    if len(sys.argv) < 2:
        print("Usage: build_chapter.py <chapter-number>")
        sys.exit(1)

    num = sys.argv[1]
    chapter = find_chapter(num)
    if not chapter:
        print(f"No chapter {num} found in {PROSE}")
        sys.exit(1)

    build(chapter)


if __name__ == "__main__":
    main()
