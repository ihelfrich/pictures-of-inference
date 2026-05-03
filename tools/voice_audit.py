#!/usr/bin/env python3
"""
Voice audit for prose files in Pictures of Inference.

Goes beyond the regex layer in `style_check.py`:
  - sentence-length statistics (rhythm, monotony)
  - parallel sentence-opening detector (3+ sentences starting the same word)
  - hedge-word density
  - AI-cadence patterns ("not just X but Y", "while X, Y")

Run with:
    python3 tools/voice_audit.py                    # audit every .qmd / .tex
    python3 tools/voice_audit.py prose/part1/*.qmd  # audit specific files

Exit code is 0 if every audit is clean by default thresholds, 1 otherwise.
"""
from __future__ import annotations
import argparse
import re
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROSE = REPO / "prose"

# Words that, when many sentences start with them in a row, suggest
# mechanical AI rhythm. (We allow some natural repetition; the alarm
# fires only on runs of 3+ in a row.)
PARALLEL_TRIGGER_WORDS = {
    "this", "that", "these", "those",
    "the", "a", "an",
    "it", "we", "you", "they",
    "here", "there", "now", "in", "on",
    "first", "second", "third", "next",
    "and", "but", "or", "so",
    "what", "when", "where", "why", "how",
    "every", "some", "many", "most",
    "sometimes", "often", "always", "never",
}

HEDGE_WORDS = {
    "perhaps", "rather", "somewhat", "fairly", "quite", "potentially",
    "essentially", "fundamentally", "ultimately", "arguably", "generally",
    "presumably", "ostensibly", "broadly", "loosely",
}

AI_CADENCE_PATTERNS = [
    (r"\bnot just\b[^.]{1,40}\bbut\b", "the 'not just X but Y' construction"),
    (r"\bisn't just\b", "the 'isn't just X' construction"),
    (r"\bmore than just\b", "the 'more than just X' construction"),
    (r"\bWhile [A-Z]", "sentence opening 'While X, Y' (overused)"),
    (r"\bAt the same time,", "the 'At the same time' transition"),
    (r"\bThat said,", "the 'That said' transition"),
    (r"\bIn other words,", "the 'In other words' transition"),
]


def strip_scaffolding(text: str) -> str:
    # Drop YAML frontmatter
    text = re.sub(r"\A---.*?---\s*", "", text, flags=re.DOTALL)
    # Drop fenced code blocks and inline code
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", "", text)
    # Drop math
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$\n]*\$", "", text)
    # Drop LaTeX commands and environments at line scale
    text = re.sub(r"\\begin\{.*?\}.*?\\end\{.*?\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", "", text)
    # Drop headings, image refs, table rows, callout fences
    text = re.sub(r"^#+ .*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"!\[.*?\]\(.*?\)\{?[^}]*\}?", "", text, flags=re.DOTALL)
    text = re.sub(r"^\|.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^:::.*$", "", text, flags=re.MULTILINE)
    # Markdown emphasis
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\*(.*?)\*", r"\1", text, flags=re.DOTALL)
    # Markdown links
    text = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", text)
    return text


def split_sentences(text: str) -> list[str]:
    text = strip_scaffolding(text)
    # Naive but reliable enough: split after .!? followed by whitespace + capital/quote
    raw = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", text)
    out = []
    for s in raw:
        s = s.strip()
        if len(s) >= 8 and re.search(r"[a-zA-Z]", s):
            out.append(s)
    return out


def word_count(s: str) -> int:
    return len(re.findall(r"\b\w+\b", s))


def sentence_stats(sentences: list[str]) -> dict:
    if not sentences:
        return None
    lens = [word_count(s) for s in sentences]
    n = len(lens)
    mean = statistics.mean(lens)
    sd = statistics.stdev(lens) if n > 1 else 0.0
    short = sum(1 for L in lens if L <= 8)
    long_ = sum(1 for L in lens if L >= 25)
    cv = (sd / mean) if mean > 0 else 0  # coefficient of variation
    return {
        "n": n,
        "mean": round(mean, 1),
        "sd": round(sd, 1),
        "min": min(lens),
        "max": max(lens),
        "short_pct": round(100 * short / n, 1),
        "long_pct": round(100 * long_ / n, 1),
        "cv": round(cv, 2),
    }


def parallel_runs(sentences: list[str]) -> list[str]:
    """Find runs of 3+ consecutive sentences starting with the same word."""
    findings = []
    starts = []
    for s in sentences:
        m = re.match(r"\s*([\"']?)(\w+)", s)
        starts.append(m.group(2).lower() if m else "")

    i = 0
    while i < len(starts):
        word = starts[i]
        run = 1
        while i + run < len(starts) and starts[i + run] == word:
            run += 1
        if run >= 3 and word in PARALLEL_TRIGGER_WORDS:
            findings.append(
                f"  ⚠ {run} consecutive sentences start with '{word}' "
                f"(near sentence {i + 1})"
            )
        i += run
    return findings


def hedge_density(sentences: list[str]) -> tuple[int, float]:
    text = " ".join(sentences).lower()
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return 0, 0.0
    hedges = sum(1 for w in words if w in HEDGE_WORDS)
    return hedges, hedges / len(words) * 1000


def cadence_hits(text: str) -> list[str]:
    found = []
    body = strip_scaffolding(text)
    for pattern, label in AI_CADENCE_PATTERNS:
        n = len(re.findall(pattern, body, flags=re.IGNORECASE))
        if n > 0:
            found.append(f"  ⚠ {n} hit(s) of {label}")
    return found


def audit(path: Path) -> tuple[bool, str]:
    raw = path.read_text()
    sents = split_sentences(raw)
    stats = sentence_stats(sents)
    if stats is None:
        return True, f"=== {path.relative_to(REPO)} ===\n  (no prose detected)"

    lines = [
        f"=== {path.relative_to(REPO)} ===",
        f"  sentences: n={stats['n']:>3} mean={stats['mean']:>4} "
        f"sd={stats['sd']:>4} min={stats['min']:>2} max={stats['max']:>3} "
        f"short={stats['short_pct']:>4}% long={stats['long_pct']:>4}% cv={stats['cv']}",
    ]

    clean = True

    # Rhythm checks
    if stats["cv"] < 0.40:
        lines.append(f"  ⚠ rhythm monotone (cv={stats['cv']} < 0.40)")
        clean = False
    if stats["short_pct"] < 8 and stats["n"] > 10:
        lines.append(f"  ⚠ too few short sentences ({stats['short_pct']}% < 8%)")
        clean = False
    if stats["long_pct"] < 5 and stats["n"] > 20:
        lines.append(f"  ⚠ too few long sentences ({stats['long_pct']}% < 5%)")
        clean = False

    # Parallel-start runs
    runs = parallel_runs(sents)
    if runs:
        clean = False
    lines.extend(runs)

    # Hedge density
    n_hedges, density = hedge_density(sents)
    if density > 4.0:
        lines.append(f"  ⚠ hedge density high: {n_hedges} words "
                     f"({density:.1f} per 1000)")
        clean = False
    elif n_hedges > 0:
        lines.append(f"  hedges: {n_hedges} ({density:.1f} per 1000)")

    # AI cadence patterns
    cad = cadence_hits(raw)
    if cad:
        clean = False
    lines.extend(cad)

    if clean and len(lines) == 2:
        lines.append("  clean")

    return clean, "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="Files or globs (default: all prose)")
    args = ap.parse_args()

    # Files that are LaTeX/Quarto scaffolding, not prose
    SCAFFOLDING = {
        "preamble.tex", "main.tex", "_quarto-preamble.tex",
    }

    if args.paths:
        targets = []
        for p in args.paths:
            path = Path(p)
            if path.is_file():
                targets.append(path)
    else:
        targets = (
            list(PROSE.rglob("*.qmd"))
            + [p for p in PROSE.rglob("*.tex") if p.name not in SCAFFOLDING]
            + list(REPO.glob("*.qmd"))
        )

    targets = sorted(set(t.resolve() for t in targets if t.is_file()))
    if not targets:
        print("No prose files found.")
        return 0

    all_clean = True
    for t in targets:
        clean, report = audit(t)
        if not clean:
            all_clean = False
        print(report)
        print()

    if not all_clean:
        print("Voice audit found issues. Review above.")
        return 1
    print("All clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
