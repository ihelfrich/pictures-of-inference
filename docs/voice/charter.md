# Voice charter

The contract. When prose drifts, point at this document, not at vibes.

This is the narrator of *Pictures of Inference*. One narrator, two authors. Both of us write toward this single voice.

---

## Five things the narrator always does

**1. Treats the reader as a fellow curious person.**
The reader is presumed intelligent. Ignorance about the topic is taken for granted; lack of capability is not. The narrator is a peer who happens to know the material, walking with the reader through it.

**2. Starts concrete and earns the abstraction.**
Every chapter, every section, every sub-argument opens with a specific thing — a number, a scene, a question someone actually asked. Generalizations arrive after the particular has done the explaining.

**3. Shows thinking, including uncertainty.**
"I don't know" and "this is genuinely contested" appear when they're true. False starts are sometimes left visible. Re-derivations on the page are encouraged — the reader watches the thought happen, rather than receiving the conclusion.

**4. Varies sentence rhythm deliberately.**
Short. Then a longer sentence that develops a thought across clauses, builds momentum, resolves where it should. Fragments where they earn their place. The reader's eye should never be able to predict the rhythm of the next sentence.

**5. Lets math be a language and parses it as one.**
Every new piece of notation gets a parsing pass on first appearance: what it says, what each piece does, what rhetorical move it makes. Equations are read aloud the first time they appear. Translation between English and math is an explicit, drilled skill, not a hidden assumption.

---

## Five things the narrator never does

**1. Performs authority.**
No "as is well known," no "it can be shown," no appeals to the reader's deference. If something is true, demonstrate it. If demonstration is out of scope, say so plainly and point at the source.

**2. Uses setup phrases.**
No "let us now turn to." No "in this section we will." No "as we'll see." The writing announces nothing. It just goes.

**3. Hedges decoratively.**
"It might perhaps be the case that in some situations" is bad writing. Hedge when uncertainty is real and name what it's about. Don't hedge to soften a confident claim.

**4. Uses em-dashes.**
Parentheses, commas, colons, or new sentences instead. This is non-negotiable, partly because em-dashes are an AI tic in 2026 and partly because the alternatives produce better rhythm.

**5. Apologizes for math.**
No "don't worry, this looks scarier than it is." No "we'll keep this brief." Math is part of the language being taught. Treating it as an alien intrusion teaches the reader to be afraid of it.

---

## Forbidden phrases

In addition to the always/never list above, these phrases are banned outright. They are AI tics, lazy transitions, or both. Caught by `tools/style_check.py` and rejected at build time.

- "Let's dive in"
- "It's important to note"
- "It is worth mentioning"
- "Needless to say"
- "In essence"
- "At its core"
- "When all is said and done"
- "It's not [X], it's [Y]"
- "[X] is more than just [Y]"
- "[X] isn't just [Y]"
- Any sentence starting with "Indeed,"
- Any sentence starting with "Importantly,"
- Any sentence starting with "Crucially,"
- Any sentence starting with "Notably,"
- Any sentence starting with "Essentially,"
- "Welcome to"
- "Get ready to"
- "Buckle up"
- "Delve into"
- "In today's world"
- Parallel triplets ("clearer, faster, better"). Two is fine. Four is fine. Three is the AI tell.

---

## On humor

Humor emerges from accuracy. When a method has a funny property, the humor is that property well-described. We do not manufacture jokes. We notice when reality is funny and point at it.

The narrator is occasionally amused. He is never trying to be amusing.

---

## On stakes

When statistics is being used or misused on real people — public policy, the replication crisis, lying-with-charts chapters — the narrator is allowed to care visibly. He does not pretend neutrality where neutrality would be a lie. He also does not lecture. He states what he thinks is true, names why, and keeps moving.

---

## The test

Read the paragraph aloud. If a human voice would naturally pause, breathe, and emphasize differently across the sentences, the rhythm is right. If every sentence has the same shape, rewrite.

Then ask: *would Feynman read this and want to keep reading?*

If yes, ship it. If no, cut.
