# Style Guide

This is the rulebook. Settled in advance so we don't relitigate during writing.

## Voice

The narrator is a wise, curious, occasionally amused traveling companion. The reader is presumed intelligent. Authority is never performed because it isn't necessary; the writing demonstrates competence by being competent.

**Always:**

- Treat the reader as a fellow curious person, not a student to be managed.
- Use simple language for complex ideas. Never simplify the ideas themselves.
- Show thinking, including uncertainty. The narrator can say "I don't know" or "this is genuinely contested."
- Vary sentence length deliberately. Short sentences for emphasis. Longer ones to develop a thought across clauses, building momentum, resolving where they should resolve.
- Use specific examples drawn from real domains.
- Acknowledge when something is hard. Do not pretend.
- Reference real history when notation, methods, or ideas have it.

**Never:**

- Use setup phrases. No "let's now turn to," no "in this section," no "as we'll see."
- Use parallel triplets ("clearer, faster, better"). They are an AI tic.
- Use em-dashes. Use parentheses, commas, colons, or sentence breaks instead.
- Manufacture humor. Humor emerges from the material when the material is funny.
- Apologize for math.
- Condescend.
- Hedge unnecessarily. "It might be argued that perhaps in some cases" is bad writing.
- Use phrases like "it's not X, it's Y" as rhetorical scaffolding.

## Sentence and paragraph rhythm

Vary lengths. The reader's eye should never be able to predict the rhythm of the next sentence.

A useful test: can the paragraph be read aloud without sounding mechanical? If a human voice would naturally pause, breathe, and emphasize differently across the sentences, the rhythm is right. If every sentence has the same shape, rewrite.

Paragraphs should also vary in length. A one-sentence paragraph is a tool. So is an eight-sentence paragraph. Pick deliberately.

## Mathematical exposition

**First principles:**

- Equations are sentences. They have subjects, predicates, and modifiers. Read them aloud the first time they appear.
- Notation is introduced once and used consistently. Every new symbol gets a parsing pass: what it says, what each piece does, what rhetorical move it makes.
- Derivations are shown when they teach something. They are skipped when they don't.
- Translation between English and mathematics is taught as a skill. Every chapter has at least one example each direction.

**Conventions:**

- $\E$ for expectation, $\Var$ for variance, $\Cov$ for covariance.
- Greek letters for population parameters. Roman letters with hats for estimators. $\mu$ vs $\bar x$, $\sigma$ vs $s$, $\beta$ vs $\hat\beta$. This distinction is taught early and respected throughout.
- Bold for vectors and matrices. $\bm{y} = \bm{X}\bm{\beta} + \bm{\varepsilon}$.
- Subscripts $i$ for individual, $t$ for time, $j$ for variable, $k$ for group when needed.
- $\log$ always means natural log unless explicitly noted.

**Boxed equations are reserved for results that the reader will use repeatedly.** Definitions and intermediate steps are not boxed. The boxes are landmarks; if everything is a landmark, nothing is.

## Figures

**Every figure carries the chapter's argument forward.** Decorative figures are removed. If the figure does not earn its place, cut it.

**Captions interpret, not just label.** A good caption says what the reader should see. "Scatter of x and y" is bad. "Wage rises with education, but the rate of increase falls after about twelve years of schooling" is good.

**Color is semantic.**

- INK (`#1a4f7a`) — primary, default, the main story.
- RUST (`#b85c38`) — treatment, contrast, the alternative perspective.
- SAGE (`#5a7247`) — control, comparison, the baseline.
- GOLD (`#b8941e`) — highlighted, derived, the synthesized quantity.
- VIOLET (`#6a5acd`) — uncertain, predicted, the model's guess.
- DIM (`#8a8a8a`) — background, de-emphasized, support.
- TEAL (`#3a8a99`) — alternative or secondary contrast when a fourth distinction is needed.

These meanings are taught in chapter three (Grammar of Graphics) and respected for the rest of the book.

**Geometric encodings follow the perceptual hierarchy.** Position over length over angle over area over color. When in doubt, position. When position is not available, length.

**Typography in figures matches the book.** Serif fonts. White backgrounds. Axis labels with units. No legend boxes when in-line labels work.

**Three sizes:** single column (4.5 inches), full width (7.0 inches), spread (10 inches for unusual cases). Authors do not invent new sizes.

## Code

**Code teaches. It does not just demonstrate.** Every code block has a purpose tied to the surrounding text.

**Tool selection:**

- Use the tool that fits the task and explain why. R for tidy applied work and statistical packages. Stata for econometric workflows where the convention is Stata. Python for general programming, machine learning, and large-scale work. SQL when data is in a database. LaTeX when typesetting matters.
- The reader is being trained as a polyglot, not a partisan.
- When introducing a tool, name what it is and what it is for. The reader should leave knowing why R is dominant in academic statistics or why Stata is common in development economics — these are facts about the world, not arbitrary preferences.

**Code style:**

- Comments explain why, not what.
- Variable names are descriptive. `x1` is a smell.
- One operation per line until the reader is fluent.
- Output is shown when it teaches. Suppressed when it doesn't.

## Citations

**This book is a scholarly work, not a textbook.** Citations are real and primary where possible. The reader is shown which papers originated which ideas and which modern treatments to consult for depth.

Format: author-year inline, full bibliography at end. Available papers are linked. Foundational works are cited even when they predate the modern restatement.

## Datasets

**Four core datasets recur.** They are introduced by name in chapter one and the reader meets them again across the book. Within each chapter, additional small datasets may appear for specific examples.

The four cores are committed to up front. They are processed and documented. The reader gets clean, ready-to-use versions.

## Layered presentation

**Each chapter has three concentric layers:**

1. **The narrative layer.** Prose with figures. No required mathematical notation beyond what was introduced earlier in the same layer. A reader who reads only this layer comes away with real conceptual understanding.

2. **The technical layer.** Set off as styled blocks ("Inside the math" or similar). Derivations, formal statements, proofs at appropriate depth. A reader who skips these blocks loses no narrative thread but gains less mathematical understanding.

3. **The frontier note.** A short closing section in every chapter, pointing to current research. Names, papers, open questions.

A reader's journey through the book is not a single line; it is a path through these layers. Some readers stay in the narrative layer throughout Parts One and Two and engage with the technical layer in Parts Three and Four. Some engage with all three layers from the start. Both readings are valid.

## Forbidden phrases

The following phrases are banned outright. They are AI tics, lazy transitions, or both:

- "Let's dive in"
- "It's important to note"
- "It is worth mentioning"
- "Needless to say"
- "In essence"
- "At its core"
- "When all is said and done"
- "It's not [X], it's [Y]"
- "[X] is more than just [Y]" or "[X] isn't just [Y]"
- Any sentence starting with "Indeed,"
- Any sentence starting with "Importantly,"
- Any sentence starting with "Crucially,"
- "Welcome to"
- "Get ready to"
- "Buckle up"

Every one of these is a sign that the writer is performing rather than thinking. Rewrite.
