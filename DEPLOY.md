# Getting *Pictures of Inference* online

Three paths, fastest to most polished.

## Option 1: GitHub Pages (recommended, ~5 minutes)

The repo already has a CI workflow at `.github/workflows/publish.yml` that builds the book on every push to `main` and deploys it to GitHub Pages.

To use it:

```bash
# from the repo root
gh repo create pictures-of-inference --public --source=. --remote=origin --push
```

Then in the repo's GitHub web UI:

1. Settings → Pages
2. Build and deployment → Source: **GitHub Actions**
3. Push any commit to `main`. The workflow runs.
4. The site appears at `https://<your-username>.github.io/pictures-of-inference/`.

The whole loop is one command + two clicks. Afterwards every push deploys automatically.

If you want a custom domain (e.g. `picturesofinference.org`):

1. Buy the domain.
2. In Settings → Pages, set the custom domain.
3. Add a DNS A record (or CNAME) pointing at GitHub Pages per their docs.

## Option 2: Quarto Publish (one-shot, no CI)

If you want to deploy a single build manually rather than wire up CI:

```bash
quarto publish gh-pages
```

This builds and pushes to a `gh-pages` branch. You configure Pages to serve from that branch (Settings → Pages → Source: Deploy from a branch → `gh-pages`).

The downside vs Option 1 is that you have to remember to run it every time the book changes. The upside is no CI to debug.

## Option 3: Netlify (if GitHub Pages is too slow or you want preview deploys for PRs)

1. Push to GitHub as in Option 1.
2. Sign in to Netlify, click "Add new site → Import from Git", point at the repo.
3. Build command: `quarto render --to html`.
4. Publish directory: `build/`.
5. Add a build environment with Python 3.11 and `pip install matplotlib numpy` in the build settings.

Netlify gives you per-PR preview URLs, which are useful when collaborating with Liz on chapters in branches.

## Working with collaborators

For Liz or any future co-author:

```bash
# Give them write access to the repo via the GitHub web UI.
# They clone:
git clone git@github.com:<your-username>/pictures-of-inference.git
cd pictures-of-inference
# Read docs/process.md, docs/voice/charter.md, docs/voice/targets.md
# Then work in a feature branch:
git checkout -b chapter-N-draft
# ...edit, commit...
git push -u origin chapter-N-draft
# Open a PR; preview deploy lands on Netlify (or equivalent).
```

## Local preview while writing

```bash
quarto preview
```

Browser opens. Edit any `.qmd`, save, watch it rebuild in about a second.

## Local full build

```bash
quarto render            # both HTML and PDF
quarto render --to html  # HTML only (skips PDF if your TeX is unhappy)
```

Output lands in `build/`. The HTML book is `build/index.html`; the PDF is `build/Pictures-of-Inference.pdf`.

## Troubleshooting

**PDF render fails with TeXLive version mismatch.** Update TeXLive (`sudo tlmgr update --self --all`) or upgrade to TeXLive 2026 (`brew install --cask mactex` on Mac). Quarto sometimes needs to install missing packages on the fly and can't reach the current CTAN repo from an old TeXLive.

**Figures don't appear.** Run `cd pictures/figures && python3 generate_all.py` to regenerate. The CI workflow does this automatically, so this should only happen locally.

**Style or voice audit failing.** `python3 tools/style_check.py` reports banned phrases. `python3 tools/voice_audit.py` reports voice rhythm issues. Both have detailed output and the latter is non-blocking by default.

**Pages deployment 404s.** First-time deploys can take a couple of minutes after the workflow succeeds. Check the Actions tab to confirm the workflow finished, then wait two more minutes.
