import math
import pytest

from geo_matcher import haversine_distance_m, match_closest


def test_haversine_zero_distance():
    p = (0.0, 0.0)
    assert haversine_distance_m(p, p) == pytest.approx(0.0, abs=1e-9)


def test_haversine_known_value_equator_1deg_lon():
    # Along the equator, 1 degree of longitude is ~111.319 km
    # Using mean Earth radius: d = R * radians(1)
    expected = 6_371_008.8 * math.radians(1.0)
    got = haversine_distance_m((0.0, 0.0), (0.0, 1.0))
    assert got == pytest.approx(expected, rel=1e-9)


def test_match_closest_basic():
    a = [(0.0, 0.0), (0.0, 2.0)]
    b = [(0.0, 1.0), (0.0, 3.0)]
    m = match_closest(a, b)

    assert m[0]["b_index"] == 0  # 0 is closer to 1 than 3
    # 2 is equidistant to 1 and 3 (1 degree each), tie-breaker picks first minimum
    assert m[1]["b_index"] == 0
    assert m[0]["distance_m"] > 0
    assert m[1]["distance_m"] > 0


def test_match_closest_empty_a():
    assert match_closest([], [(0.0, 0.0)]) == []


def test_match_closest_empty_b_raises():
    with pytest.raises(ValueError):
        match_closest([(0.0, 0.0)], [])
