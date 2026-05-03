#!/usr/bin/env python3
"""
Style check the prose. Fails loudly when banned phrases are found.

Run with: make check  or  python tools/style_check.py

Exit codes:
    0  clean
    1  violations found
"""

from __future__ import annotations
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
PROSE = REPO / "prose"


# Phrases that should never appear. Case-insensitive substring match.
BANNED_PHRASES = [
    "let's dive in",
    "it's important to note",
    "it is worth mentioning",
    "needless to say",
    "in essence",
    "at its core",
    "when all is said and done",
    "welcome to",
    "get ready to",
    "buckle up",
    "delve into",
    "in today's world",
    "in this section we will",
    "in this section, we will",
    "let's now turn to",
    "as we'll see",
    "as we will see",
    "in this chapter we will",
    "in this chapter, we will",
]

# Sentence-starts that should not appear at the beginning of a sentence.
BANNED_STARTS = [
    "indeed,",
    "importantly,",
    "crucially,",
    "notably,",
    "essentially,",
]

# Patterns. The em-dash matters.
BANNED_PATTERNS = [
    (r"—", "em-dash (use parentheses, commas, colons, or periods)"),
    (r"\bit's not\b.{1,30}\bit's\b", "the 'it's not X, it's Y' framing"),
    (r"\bisn't just\b", "the 'isn't just X' framing"),
    (r"\bmore than just\b", "the 'more than just X' framing"),
]


def is_in_comment_or_code(line: str, idx: int) -> bool:
    """Skip if the match is inside a LaTeX comment or a verbatim block."""
    before = line[:idx]
    return "%" in before


def check_file(path: Path) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []
    in_lstlisting = False

    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw

        # Skip code blocks
        stripped = line.strip()
        if stripped.startswith(r"\begin{lstlisting}"):
            in_lstlisting = True
            continue
        if stripped.startswith(r"\end{lstlisting}"):
            in_lstlisting = False
            continue
        if in_lstlisting:
            continue
        # Skip pure comments
        if stripped.startswith("%"):
            continue

        lower = line.lower()

        # Phrase scan
        for phrase in BANNED_PHRASES:
            idx = lower.find(phrase)
            if idx >= 0 and not is_in_comment_or_code(line, idx):
                violations.append((lineno, f"banned phrase: {phrase!r}"))

        # Sentence-start scan
        for start in BANNED_STARTS:
            for m in re.finditer(
                rf"(?:^|[.!?]\s+){re.escape(start)}", lower
            ):
                if not is_in_comment_or_code(line, m.start()):
                    violations.append(
                        (lineno, f"banned sentence start: {start!r}")
                    )

        # Pattern scan
        for pattern, label in BANNED_PATTERNS:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                if not is_in_comment_or_code(line, m.start()):
                    violations.append((lineno, label))

    return violations


def main():
    prose_files = sorted(
        list(PROSE.rglob("*.tex")) + list(PROSE.rglob("*.qmd"))
    )
    # Also scan top-level .qmd files (index, preface, etc.).
    prose_files += sorted(REPO.glob("*.qmd"))
    if not prose_files:
        print("No prose files found in", PROSE)
        return 0

    total = 0
    for f in prose_files:
        violations = check_file(f)
        if violations:
            relative = f.relative_to(REPO)
            for lineno, msg in violations:
                print(f"{relative}:{lineno}: {msg}")
            total += len(violations)

    if total > 0:
        print(f"\n{total} violation(s).")
        return 1
    print("Clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
