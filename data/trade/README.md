# Trade and Bilateral Flow Data

This folder is the home of the trade-related datasets that thread through the book.

## What goes here

- **The bilateral trade panel** that anchors many examples. Provenance and structure documented in this README.
- **Cleaned subsets** for specific chapters where the full panel would be too much.
- **A processing script** (`process.R` or `process.py`) that takes raw input and produces analysis-ready output.

## Recommended structure

```
data/trade/
├── README.md          (this file)
├── process.R          (or process.py) — cleaning script
├── raw/               (gitignored — original source files)
├── clean/             (versioned — analysis-ready)
│   ├── bilateral_panel.csv
│   ├── countries.csv
│   └── ...
└── codebook.md        (variable definitions, units, sources)
```

## What the early chapters need

Chapters 1-6 use this dataset. The minimum slice they need:

- 8-15 countries
- 15-25 years
- For each country-year-partner triple: bilateral exports, bilateral imports, GDP of both, distance, common language, common border
- Optionally: trade-cost estimates if Ian's panel includes them

Reasonable ~5000 row CSV. If Ian's `EffDist_V2026` panel can provide a slice like this, that's what we use. Otherwise we use BACI or COMTRADE as placeholder until Ian's data is processed.

## Sources to credit

When the real dataset lands, this section should list:

- Where the raw data came from.
- What processing was done to it.
- Any caveats about coverage or measurement.
- The license and how the dataset can be redistributed.

## Status

**Not yet populated.** The dataset goes in here as the next major action.
