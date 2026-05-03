"""
Dataset loaders for Pictures of Inference.

Use:
    from poi.data import trade
    rows = trade()                       # list of dicts
    df = trade(as_dataframe=True)        # pandas DataFrame (requires pandas)

Each loader resolves paths relative to the repo root, so it works
regardless of the working directory.
"""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data"


def _read_csv_typed(path: Path, types: dict) -> list[dict]:
    """Read a CSV, casting columns by `types` mapping (col -> callable)."""
    rows: list[dict] = []
    with path.open(newline="") as f:
        for raw in csv.DictReader(f):
            row = {}
            for k, v in raw.items():
                cast = types.get(k, str)
                row[k] = cast(v)
            rows.append(row)
    return rows


def trade(as_dataframe: bool = False):
    """Load the bilateral trade panel.

    Returns either a list of dicts (default) or a pandas DataFrame.
    Synthetic placeholder until the EffDist_V2026 slice replaces it.
    """
    path = DATA_DIR / "trade" / "clean" / "bilateral_panel.csv"
    types = {
        "year": int,
        "exporter": str,
        "importer": str,
        "exports_usd_millions": float,
        "gdp_exporter_trillions": float,
        "gdp_importer_trillions": float,
        "distance_km": float,
        "common_language": int,
        "common_border": int,
    }
    rows = _read_csv_typed(path, types)
    if as_dataframe:
        import pandas as pd
        return pd.DataFrame(rows)
    return rows


def column(rows: Iterable[dict], name: str):
    """Extract one column from a list-of-dicts as a list."""
    return [r[name] for r in rows]


__all__ = ["trade", "column", "REPO_ROOT", "DATA_DIR"]
