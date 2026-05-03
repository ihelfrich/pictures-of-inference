# Voice Samples

This folder is where the book's voice gets calibrated. Until samples are here, drafted chapters are approximations.

## What to put here

Files named `ian-001.md`, `ian-002.md`, etc. for Ian's writing.
Files named `liz-001.md`, `liz-002.md`, etc. for Liz's writing.

Each file contains one piece of writing that exemplifies the voice you want this book to have. A few suggestions for sources:

- A paragraph from a paper that's especially well-written.
- An email to a student where you explained something well.
- A blog post or research note.
- A piece of lecture material that worked.
- Anything where you sound like yourself on a quantitative subject and you'd be proud to have it represent you.

## What makes a good sample

- Long enough to show rhythm. Two paragraphs minimum, ideally three to five.
- Substantive content. Not throat-clearing or transitions. The actual exposition.
- Voice you want emulated, not voice you're stuck with. If you have something that's *almost* the voice, label it as such; it's still useful as a target.

## What to avoid

- Drafts you wouldn't want to read aloud.
- Pure formal academic prose if that's not the voice you want.
- Anything that violates the style guide; we'd be calibrating to bad habits.

## How Claude uses these

At the start of any chapter-writing session, Claude reads every file here. Claude tries to match the rhythm, vocabulary, and cadence. The more samples available, the more accurate the match.

Three samples is the floor for serious calibration. Six to ten is ideal. More than ten is overkill but harmless.

## Format notes

Plain markdown. No special structure required. Optional front matter:

```
---
source: "Email to John Hagberd, 2025-04-12"
context: "Explaining elasticity intuitively"
target: "as-is" or "approximation" or "aspirational"
---

The actual prose goes here...
```

The `target` field tells Claude whether this is your current voice (use as-is), close to your current voice (good approximation), or the voice you'd like to write in (aspire toward).
