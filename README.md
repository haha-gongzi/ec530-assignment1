# Assignment 1 — Geo Location Nearest-Neighbor Matcher

**Goal:** Given two arrays of GPS coordinates (latitude, longitude), match each point in the first array to the *closest* point in the second array.

This repository provides a small, developer-friendly Python module with:
- A correct great-circle distance implementation (Haversine).
- A matcher function that returns nearest neighbors + distances.
- Unit tests (pytest).
- Linting configuration (flake8).
- Clear README and examples.

---

## Install

### Option A: install in editable mode (recommended for development)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

---

## Usage

```python
from geo_matcher import match_closest

a = [(42.3601, -71.0589), (42.3473, -71.0825)]  # points to match
b = [(42.3662, -71.0621), (42.3496, -71.0995)]  # candidate points

matches = match_closest(a, b)
for m in matches:
    print(m)
```

Output is a list of dicts (one per point in `a`):

```text
{'a_index': 0, 'a_point': (42.3601, -71.0589), 'b_index': 0, 'b_point': (42.3662, -71.0621), 'distance_m': 716.3}
...
```

---

## API

### `haversine_distance_m(p1, p2) -> float`
Returns great-circle distance in meters between two `(lat, lon)` points in degrees.

### `match_closest(a_points, b_points) -> list[dict]`
For each point in `a_points`, finds the closest point in `b_points`.

**Edge cases**
- If `a_points` is empty: returns `[]`.
- If `b_points` is empty: raises `ValueError`.

---

## Run tests

```bash
pytest -q
```

---

## Lint (flake8)

```bash
flake8
```

---

## Notes on distance formula (Haversine)

GPS coordinates lie on (approximately) a sphere. The Haversine formula computes the great-circle distance:

1. Convert degrees to radians.
2. Compute:
   - `dlat = lat2 - lat1`
   - `dlon = lon2 - lon1`
   - `a = sin²(dlat/2) + cos(lat1)cos(lat2)sin²(dlon/2)`
   - `c = 2 * atan2(√a, √(1-a))`
3. Distance: `d = R * c`, where `R ≈ 6371008.8 m` (mean Earth radius).

This is accurate enough for most software engineering tasks unless you need ellipsoidal geodesics.

---

## Repository structure

```
.
├─ src/
│  └─ geo_matcher/
│     ├─ __init__.py
│     └─ matcher.py
├─ tests/
│  └─ test_matcher.py
├─ pyproject.toml
├─ .flake8
├─ .gitignore
└─ README.md
```
