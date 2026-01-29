from geo_matcher.airports import Airport, closest_airport


def test_closest_airport_basic():
    airports = [
        Airport(code="BOS", name="Boston Logan", lat=42.3656, lon=-71.0096),
        Airport(code="JFK", name="John F. Kennedy", lat=40.6413, lon=-73.7781),
    ]

    ap, dist_m = closest_airport((42.3601, -71.0589), airports)
    assert ap.code == "BOS"
    assert 0 < dist_m < 20_000
