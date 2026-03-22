"""Tests for GET /api/v1/health"""


def test_health_returns_ok(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_health_timestamp_is_iso8601(client):
    """Timestamp must be parseable as ISO 8601."""
    from datetime import datetime

    resp = client.get("/api/v1/health")
    ts = resp.json()["timestamp"]
    # datetime.fromisoformat handles +00:00 suffix; raises if invalid
    dt = datetime.fromisoformat(ts)
    assert dt.year >= 2024
