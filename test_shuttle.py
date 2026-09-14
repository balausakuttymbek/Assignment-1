import pytest

from shuttle_logic import parse_event, validate_event
from analysis import analyze
from data import raw_data
from main import occupancy_category


def test_valid_event_passes():
    raw = {"Timestamp": "08:00", "Route": "x", "Bus": "B01", "Passengers": 18, "Speed_kmh": 31, "Status": "ON_ROUTE"}
    parsed = parse_event(raw)
    is_valid, reason = validate_event(parsed)
    assert is_valid is True


def test_negative_passengers_rejected():
    raw = {"Timestamp": "08:00", "Route": "x", "Bus": "B01", "Passengers": -3, "Speed_kmh": 20, "Status": "ON_ROUTE"}
    parsed = parse_event(raw)
    is_valid, reason = validate_event(parsed)
    assert is_valid is False


def test_speed_out_of_range_rejected():
    raw = {"Timestamp": "08:00", "Route": "x", "Bus": "B01", "Passengers": 20, "Speed_kmh": 250, "Status": "ON_ROUTE"}
    parsed = parse_event(raw)
    is_valid, reason = validate_event(parsed)
    assert is_valid is False


def test_bad_timestamp_does_not_crash():
    from shuttle_logic import event_generator
    bad = [{"Timestamp": "25:99", "Route": "x", "Bus": "B01", "Passengers": -5, "Speed_kmh": 999, "Status": "FLYING"}]
    results = list(event_generator(bad))
    assert results[0]["is_valid"] is False


def test_analysis_matches_hand_calculation():
    results = analyze(raw_data)
    assert results["average_passengers"] == 24.4
    assert results["max_passengers"] == 30
    assert results["stopped_events"] == 1
    assert results["busiest_bus"] == "B02"


@pytest.mark.parametrize("passengers,expected", [
    (0, "LOW"),
    (10, "LOW"),
    (11, "MEDIUM"),
    (20, "MEDIUM"),
    (21, "HIGH"),
    (30, "HIGH"),
    (31, "OVER_CAPACITY"),
    (60, "OVER_CAPACITY"),
])
def test_occupancy_category_boundaries(passengers, expected):
    assert occupancy_category(passengers) == expected