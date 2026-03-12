# tests/test_config.py
import pytest
from app.config import load_config, save_config

def test_load_config_returns_defaults(tmp_path):
    path = str(tmp_path / "config.yaml")
    data = {
        "reset_hour": 0,
        "poll_interval": 5,
        "alert_threshold": 3.0,
        "alert_window_min": 5,
        "symbols": ["BNB", "BTC", "VET", "VTHO", "ETH"],
        "email": {"enabled": False},
        "telegram": {"enabled": False},
    }
    save_config(path, data)
    cfg = load_config(path)
    assert cfg["reset_hour"] == 0
    assert cfg["poll_interval"] == 5
    assert cfg["alert_threshold"] == 3.0
    assert cfg["symbols"] == ["BNB", "BTC", "VET", "VTHO", "ETH"]

def test_save_and_reload_config(tmp_path):
    path = str(tmp_path / "config.yaml")
    data = {"reset_hour": 6, "poll_interval": 10, "alert_threshold": 5.0,
            "alert_window_min": 10, "symbols": ["BTC"],
            "email": {"enabled": False}, "telegram": {"enabled": False}}
    save_config(path, data)
    loaded = load_config(path)
    assert loaded["reset_hour"] == 6
    assert loaded["poll_interval"] == 10
