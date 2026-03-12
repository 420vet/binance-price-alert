# tests/test_api.py
import pytest
from fastapi.testclient import TestClient

def get_client():
    from main import app
    return TestClient(app)

def test_get_config_returns_200():
    client = get_client()
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "poll_interval" in data
    assert "alert_threshold" in data
    assert "symbols" in data

def test_post_config_updates_values():
    client = get_client()
    response = client.post("/config", json={
        "poll_interval": 10,
        "alert_threshold": 5.0,
        "alert_window_min": 10,
        "reset_hour": 1,
        "symbols": ["BTC", "ETH"],
        "email": {"enabled": False},
        "telegram": {"enabled": False},
    })
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_index_returns_html():
    client = get_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
