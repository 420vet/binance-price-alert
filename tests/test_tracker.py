# tests/test_tracker.py
import time
from app.tracker import PriceTracker

def test_no_spike_below_threshold():
    tracker = PriceTracker(threshold_pct=3.0, window_min=5)
    tracker.record("BTC", {"usdt": 65000.0, "eur": 60000.0})
    time.sleep(0.01)
    tracker.record("BTC", {"usdt": 65100.0, "eur": 60092.0})
    result = tracker.get_snapshot("BTC", day_open=65000.0)
    assert result["spike_alert"] is False
    assert result["change_spike_pct"] < 3.0

def test_spike_detected_above_threshold():
    tracker = PriceTracker(threshold_pct=3.0, window_min=5)
    tracker.record("BTC", {"usdt": 65000.0, "eur": 60000.0})
    time.sleep(0.01)
    tracker.record("BTC", {"usdt": 67200.0, "eur": 61900.0})
    result = tracker.get_snapshot("BTC", day_open=65000.0)
    assert result["spike_alert"] is True
    assert result["change_spike_pct"] > 3.0

def test_change_day_pct_calculated_correctly():
    tracker = PriceTracker(threshold_pct=3.0, window_min=5)
    tracker.record("BTC", {"usdt": 66300.0, "eur": 61100.0})
    result = tracker.get_snapshot("BTC", day_open=65000.0)
    assert round(result["change_day_pct"], 2) == 2.0

def test_returns_empty_snapshot_for_unknown_symbol():
    tracker = PriceTracker(threshold_pct=3.0, window_min=5)
    result = tracker.get_snapshot("XYZ", day_open=0.0)
    assert result["usdt"] == 0.0
