# Bilateral Trade Panel — Codebook

**STATUS: SYNTHETIC PLACEHOLDER.** Numbers fabricated by `process.py` to be roughly gravity-model-shaped. Do not cite as real data. Swap for the EffDist_V2026 slice (or a BACI / COMTRADE extract) before any chapter ships beyond drafts.

## File

`clean/bilateral_panel.csv` — 300 rows (6 exporters × 5 importers × 10 years).

## Variables

| Variable | Type | Description |
|---|---|---|
| `year` | int | Year of observation, 2014-2023 |
| `exporter` | str | ISO3 country code of exporting country |
| `importer` | str | ISO3 country code of importing country |
| `exports_usd_millions` | float | Bilateral exports, USD millions |
| `gdp_exporter_trillions` | float | Exporter GDP, USD trillions |
| `gdp_importer_trillions` | float | Importer GDP, USD trillions |
| `distance_km` | float | Great-circle distance between country centroids, km |
| `common_language` | int | 1 if exporter and importer share an official language, else 0 |
| `common_border` | int | 1 if countries share a land border, else 0 |

## Countries

USA, CHN, DEU, JPN, GBR, KOR. Six chosen for size and student recognizability.

## Generation

Run `python data/trade/process.py` from the repo root. Seed is fixed (2026), so the file is deterministic.

## Replacement

When real data lands:

1. Replace `process.py` with the real cleaning script.
2. Update this codebook with provenance, units, and any quirks.
3. Update `data/trade/README.md` with sources and license.
4. Re-run `process.py` to produce the new `clean/bilateral_panel.csv`.
5. Verify all chapters that load this dataset still render.
