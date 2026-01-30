from pathlib import Path
import pytest

from geo_matcher.airports import load_airports_csv


def test_load_airports_csv(tmp_path: Path):
    csv_text = (
        "code,name,lat,lon\n"
        "BOS,Boston Logan,42.3656,-71.0096\n"
        "JFK,John F. Kennedy,40.6413,-73.7781\n"
    )
    p = tmp_path / "airports.csv"
    p.write_text(csv_text, encoding="utf-8")

    airports = load_airports_csv(p)
    assert len(airports) == 2
    assert airports[0].code == "BOS"


def test_load_airports_csv_missing_header(tmp_path: Path):
    p = tmp_path / "airports.csv"
    p.write_text("BOS,Boston Logan,42.3656,-71.0096\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_airports_csv(p)
