"""
Placeholder synthetic bilateral trade panel for early-chapter examples.

Produces:
  data/trade/clean/bilateral_panel.csv

Schema:
  year, exporter, importer, exports_usd_millions,
  gdp_exporter_trillions, gdp_importer_trillions,
  distance_km, common_language, common_border

Coverage:
  - 6 countries: USA, CHN, DEU, JPN, GBR, KOR
  - 10 years: 2014-2023
  - All ordered exporter-importer pairs (30 dyads per year)
  - 300 rows total

STATUS: SYNTHETIC PLACEHOLDER. Numbers are fabricated to be roughly
plausible (gravity-model-shaped) so figures and prose can be drafted
against real-feeling structure. Do not cite. Swap for the real
EffDist_V2026 slice (or a BACI / COMTRADE extract) before any chapter
ships beyond drafts.
"""

from __future__ import annotations
import csv
import math
import random
from pathlib import Path

random.seed(2026)

COUNTRIES = {
    # iso3 -> (gdp_2023_usd_trillions, lat, lon, official_lang)
    "USA": (27.36, 38.0, -97.0, "en"),
    "CHN": (17.79, 35.0, 105.0, "zh"),
    "DEU": (4.46, 51.2, 10.4, "de"),
    "JPN": (4.21, 36.2, 138.3, "ja"),
    "GBR": (3.34, 54.0, -2.0, "en"),
    "KOR": (1.71, 36.5, 127.9, "ko"),
}

# No land borders among this set (all separated by water or other countries).
BORDERS: set[tuple[str, str]] = set()

YEARS = range(2014, 2024)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def gdp_at_year(gdp_2023: float, year: int) -> float:
    """Roughly 4% nominal growth back from 2023."""
    years_back = 2023 - year
    return gdp_2023 / (1.04 ** years_back)


def main() -> None:
    out = Path(__file__).parent / "clean" / "bilateral_panel.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for year in YEARS:
        for ex, (gdp_ex_2023, lat_ex, lon_ex, lang_ex) in COUNTRIES.items():
            for im, (gdp_im_2023, lat_im, lon_im, lang_im) in COUNTRIES.items():
                if ex == im:
                    continue
                gdp_ex = gdp_at_year(gdp_ex_2023, year)
                gdp_im = gdp_at_year(gdp_im_2023, year)
                dist = haversine_km(lat_ex, lon_ex, lat_im, lon_im)
                same_lang = int(lang_ex == lang_im)
                same_border = int((ex, im) in BORDERS or (im, ex) in BORDERS)
                # Gravity-flavored synthetic exports.
                # Gravity intercept tuned so USA-CHN 2023 lands near
                # ~$150 billion (real-ballpark) for plausibility.
                log_ex = (
                    7.0
                    + 0.95 * math.log(gdp_ex)
                    + 0.85 * math.log(gdp_im)
                    - 0.85 * math.log(dist)
                    + 0.40 * same_lang
                    + 0.30 * same_border
                    + random.gauss(0.0, 0.25)
                )
                exports = math.exp(log_ex) * 1000.0  # USD millions
                rows.append(
                    {
                        "year": year,
                        "exporter": ex,
                        "importer": im,
                        "exports_usd_millions": round(exports, 1),
                        "gdp_exporter_trillions": round(gdp_ex, 3),
                        "gdp_importer_trillions": round(gdp_im, 3),
                        "distance_km": round(dist, 0),
                        "common_language": same_lang,
                        "common_border": same_border,
                    }
                )

    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
