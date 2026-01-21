"""
geo_matcher.matcher

Core functionality:
- Haversine great-circle distance between two GPS points.
- Match each point in list A to the closest point in list B.

Coordinates are tuples: (latitude_degrees, longitude_degrees)
Latitude range:  [-90, 90]
Longitude range: [-180, 180]
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, radians, sin, sqrt
from typing import Iterable, List, Sequence, Tuple, Dict, Any


# Mean Earth radius in meters (IUGG recommended mean radius)
EARTH_RADIUS_M = 6_371_008.8


LatLon = Tuple[float, float]


@dataclass(frozen=True)
class MatchResult:
    """One nearest-neighbor match from A -> B."""
    a_index: int
    a_point: LatLon
    b_index: int
    b_point: LatLon
    distance_m: float

    def as_dict(self) -> Dict[str, Any]:
        return {
            "a_index": self.a_index,
            "a_point": self.a_point,
            "b_index": self.b_index,
            "b_point": self.b_point,
            "distance_m": self.distance_m,
        }


def _validate_point(p: LatLon) -> None:
    lat, lon = p
    if not (-90.0 <= lat <= 90.0):
        raise ValueError(f"Latitude must be in [-90, 90], got {lat}")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError(f"Longitude must be in [-180, 180], got {lon}")


def haversine_distance_m(p1: LatLon, p2: LatLon) -> float:
    """
    Compute great-circle distance (meters) between two GPS points using Haversine.

    Args:
        p1, p2: (lat_deg, lon_deg)

    Returns:
        Distance in meters (float).
    """
    _validate_point(p1)
    _validate_point(p2)

    lat1, lon1 = p1
    lat2, lon2 = p2

    # Convert to radians
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi / 2.0) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2.0) ** 2
    c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a))
    return EARTH_RADIUS_M * c


def match_closest(
    a_points: Sequence[LatLon],
    b_points: Sequence[LatLon],
) -> List[Dict[str, Any]]:
    """
    Match each point in A to the closest point in B (by Haversine distance).

    Args:
        a_points: list/tuple of (lat, lon)
        b_points: list/tuple of (lat, lon)

    Returns:
        List of dictionaries (one per a_points element) containing:
        - a_index, a_point
        - b_index, b_point
        - distance_m

    Raises:
        ValueError: if b_points is empty or any coordinate is out of range.
    """
    if len(b_points) == 0:
        raise ValueError("b_points must not be empty (cannot match to an empty set).")

    # validate upfront to fail fast (helpful for other developers)
    for p in a_points:
        _validate_point(p)
    for p in b_points:
        _validate_point(p)

    results: List[MatchResult] = []

    for i, ap in enumerate(a_points):
        best_j = 0
        best_dist = float("inf")
        for j, bp in enumerate(b_points):
            d = haversine_distance_m(ap, bp)
            if d < best_dist:
                best_dist = d
                best_j = j
        results.append(MatchResult(i, ap, best_j, b_points[best_j], best_dist))

    return [r.as_dict() for r in results]
