from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from .matcher import haversine_distance_m


@dataclass(frozen=True)
class Airport:
    code: str
    name: str
    lat: float
    lon: float


def load_airports_csv(path: str | Path) -> List[Airport]:
    """
    Load airports from a CSV file with header: code,name,lat,lon
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p}")

    airports: List[Airport] = []
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")

        fields = {h.strip().lower(): h for h in reader.fieldnames}
        required = {"code", "name", "lat", "lon"}
        if not required.issubset(fields.keys()):
            raise ValueError(f"CSV must contain header: {sorted(required)}")

        for row in reader:
            code = (row[fields["code"]] or "").strip()
            name = (row[fields["name"]] or "").strip()
            lat = float(row[fields["lat"]])
            lon = float(row[fields["lon"]])
            airports.append(Airport(code=code, name=name, lat=lat, lon=lon))

    if not airports:
        raise ValueError("No airports loaded from CSV")
    return airports


def closest_airport(
    location: Tuple[float, float],
    airports: Iterable[Airport],
) -> Tuple[Airport, float]:
    """
    Find the closest airport to a (lat, lon). Returns (airport, distance_m).
    """
    lat, lon = location
    best: Optional[Airport] = None
    best_dist: float = float("inf")

    for ap in airports:
        d = haversine_distance_m(lat, lon, ap.lat, ap.lon)
        if d < best_dist:
            best_dist = d
            best = ap

    if best is None:
        raise ValueError("airports is empty")
    return best, best_dist
