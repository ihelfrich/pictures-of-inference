# Pictures of Inference

A book by Dr. Ian Helfrich and Dr. Elizaveta Gonchar.

A complete visual course in statistics, calculus, and econometrics — from "what is a correlation" to research-grade econometric theory. Heavy on visualization. Math taught as a language. Multiple data types treated as first-class citizens rather than tidy rectangles.

## How to read this repo

If you are Claude Code: read in this order.

1. `docs/proposal.md` — what this book is and who it's for.
2. `docs/style-guide.md` — voice, conventions, banned phrases. Not negotiable.
3. `docs/table-of-contents.md` — the chapter map across four parts.
4. `docs/dataset-inventory.md` — the data we have and need.
5. `docs/voice/` — voice samples from Ian and Liz. Read every file here before drafting anything.

Then look at `prose/` to see what's been drafted, `pictures/` to see the figure system, and `drafts/` to see the v3 material we're rewriting from.

If you are a human collaborator: same order, then jump to whichever part you're working on.

## Project status

We are at the architecture-committed, drafting-not-yet-started point. The v3 textbook in `drafts/` is the previous incarnation — we are rewriting from scratch with the new architecture but keeping useful prose, figures, and code patterns.

**Next concrete steps in priority order:**

1. Voice samples land in `docs/voice/` from Ian and Liz.
2. Real data lands in `data/` (at minimum, a trade panel slice for the early chapters).
3. Chapter 1 ("Numbers on the Page") gets drafted in `prose/part1/`.
4. Iterate on chapter 1 until voice is right.
5. Use chapter 1 as template for chapters 2-6.
6. Deliver chapters 1-6 to Ian's students.
7. Then plan the rest of the book.

## Repo layout

```
poi/
├── README.md              # this file
├── Makefile               # build system
├── _quarto.yml            # Quarto config (when we migrate)
├── .gitignore
│
├── docs/                  # design documents
│   ├── proposal.md
│   ├── style-guide.md
│   ├── table-of-contents.md
│   ├── dataset-inventory.md
│   ├── voice/             # voice samples — READ BEFORE WRITING
│   └── reference/         # references and notes
│
├── prose/                 # the book itself
│   ├── front/             # preface, field guide
│   ├── part1/             # How to See
│   ├── part2/             # How to Speak
│   ├── part3/             # How to Think
│   ├── part4/             # How to Discover
│   ├── back/              # appendices, bibliography
│   ├── preamble.tex       # shared LaTeX preamble
│   └── main.tex           # driver file
│
├── pictures/              # the figure system
│   ├── lib/               # plotting library (poi/style/poi.py)
│   ├── style/             # palette, fonts, conventions
│   └── figures/           # one Python script per chapter
│
├── data/                  # datasets
│   ├── trade/
│   ├── geospatial/
│   ├── psychology/
│   ├── timeseries/
│   └── examples/          # smaller datasets for specific chapters
│
├── drafts/                # the v3 book we're rewriting from
│   ├── v3-chapters/
│   ├── v3-figures/
│   └── v3-main.tex
│
├── build/                 # compiled output (gitignored)
│   ├── pdf/
│   └── html/
│
├── tools/                 # helper scripts
│
└── .claude/               # Claude Code project notes
    └── CLAUDE.md          # project-specific instructions
```

## How to build

From the repo root:

```bash
# Build the current state of the book to PDF
make pdf

# Regenerate all figures
make figures

# Clean build artifacts
make clean

# Build a single chapter (e.g., 01)
make ch01
```

The Makefile drives both LaTeX and the figure generation system. Whenever you change a figure script, run `make figures` to regenerate. Whenever you change prose, run `make pdf` to rebuild.

Build cycle should be under 30 seconds for the whole book. If it isn't, that's a bug to fix.

## How to write a chapter

Chapter files live in `prose/part1/`, `prose/part2/`, etc., named like `01-numbers-on-the-page.tex`. Each chapter has a corresponding figure script in `pictures/figures/ch01.py` that generates everything that chapter needs.

The chapter file uses the shared preamble and the standard environments (`keyinsight`, `tryitnow`, `inthemath`, `frontiernote`, `expedition`). See `prose/preamble.tex` for what's available.

Voice rules in `docs/style-guide.md` are mandatory. The forbidden-phrases list in particular is strictly enforced.

## How to add a figure

Add a function to the chapter's figure script:

```python
# pictures/figures/ch01.py
from poi.style import poi_style, INK, RUST, SAGE
import matplotlib.pyplot as plt

@poi_style
def fig_data_rectangle(ax):
    # ... plotting code ...
    pass
```

Then in the chapter:

```latex
\begin{figure}[ht]
\centering
\includegraphics[width=\linewidth]{fig_data_rectangle.pdf}
\caption{Caption that interprets the figure, not just labels it.}
\label{fig:data-rectangle}
\end{figure}
```

Run `make figures` to regenerate. The figure system handles styling, sizing, and saving.

## Datasets

Core datasets live in `data/`. Each has its own subdirectory with the raw data, a processing script, and a README explaining sources and provenance. The early chapters use the trade panel; later chapters layer in the others.

If a dataset is too large or licensing-restricted for the public repo, it goes in `data/.local/` (gitignored) with a `data/sources.md` entry explaining how to obtain it.

## Authorship and license

Co-authored by Dr. Ian Helfrich and Dr. Elizaveta Gonchar.

Prose: Creative Commons Attribution-ShareAlike (CC BY-SA 4.0).
Code and figures: MIT License.
Datasets: per-dataset, documented in `data/*/README.md`.
