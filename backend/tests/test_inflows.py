"""Tests for /api/v1/inflows — CRUD + pagination + month filter."""


def _create_inflow(client, amount=1000.0, date="2026-03-15", source="Salary", **kwargs):
    payload = {"amount": amount, "date": date, "source": source, **kwargs}
    return client.post("/api/v1/inflows", json=payload)


# ── Create ───────────────────────────────────────────────────────────────────

def test_create_inflow_happy_path(client):
    resp = _create_inflow(client)
    assert resp.status_code == 201
    data = resp.json()
    assert data["amount"] == 1000.0
    assert data["date"] == "2026-03-15"
    assert data["source"] == "Salary"
    assert data["categoryId"] is None
    assert "id" in data
    assert "createdAt" in data


def test_create_inflow_with_category(client, seed_inflow_category):
    resp = _create_inflow(client, categoryId=seed_inflow_category.id)
    assert resp.status_code == 201
    assert resp.json()["categoryId"] == seed_inflow_category.id


def test_create_inflow_invalid_amount_zero(client):
    resp = _create_inflow(client, amount=0)
    assert resp.status_code == 422


def test_create_inflow_invalid_amount_negative(client):
    resp = _create_inflow(client, amount=-50.0)
    assert resp.status_code == 422


def test_create_inflow_invalid_date_format(client):
    resp = _create_inflow(client, date="15-03-2026")
    assert resp.status_code == 422


def test_create_inflow_missing_source(client):
    resp = client.post("/api/v1/inflows", json={"amount": 100.0, "date": "2026-03-01"})
    assert resp.status_code == 422


# ── Get ──────────────────────────────────────────────────────────────────────

def test_get_inflow_found(client):
    inflow_id = _create_inflow(client).json()["id"]
    resp = client.get(f"/api/v1/inflows/{inflow_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == inflow_id


def test_get_inflow_not_found(client):
    assert client.get("/api/v1/inflows/99999").status_code == 404


# ── Update ───────────────────────────────────────────────────────────────────

def test_patch_inflow_partial(client):
    inflow_id = _create_inflow(client, amount=500.0).json()["id"]
    resp = client.patch(f"/api/v1/inflows/{inflow_id}", json={"amount": 750.0})
    assert resp.status_code == 200
    data = resp.json()
    assert data["amount"] == 750.0
    assert data["source"] == "Salary"  # unchanged


def test_patch_inflow_not_found(client):
    assert client.patch("/api/v1/inflows/99999", json={"amount": 100.0}).status_code == 404


def test_patch_inflow_invalid_amount(client):
    inflow_id = _create_inflow(client).json()["id"]
    resp = client.patch(f"/api/v1/inflows/{inflow_id}", json={"amount": -1.0})
    assert resp.status_code == 422


# ── Delete ───────────────────────────────────────────────────────────────────

def test_delete_inflow_happy_path(client):
    inflow_id = _create_inflow(client).json()["id"]
    assert client.delete(f"/api/v1/inflows/{inflow_id}").status_code == 204
    assert client.get(f"/api/v1/inflows/{inflow_id}").status_code == 404


def test_delete_inflow_not_found(client):
    assert client.delete("/api/v1/inflows/99999").status_code == 404


# ── List / pagination ─────────────────────────────────────────────────────────

def test_list_inflows_empty(client):
    resp = client.get("/api/v1/inflows")
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["limit"] == 20


def test_list_inflows_pagination(client):
    for i in range(5):
        _create_inflow(client, amount=100.0 + i, source=f"Source{i}")

    resp = client.get("/api/v1/inflows?page=1&limit=3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["data"]) == 3
    assert data["page"] == 1
    assert data["limit"] == 3

    resp2 = client.get("/api/v1/inflows?page=2&limit=3")
    data2 = resp2.json()
    assert len(data2["data"]) == 2


def test_list_inflows_month_filter(client):
    _create_inflow(client, amount=1000.0, date="2026-03-10", source="March")
    _create_inflow(client, amount=2000.0, date="2026-04-05", source="April")

    resp = client.get("/api/v1/inflows?month=2026-03")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["data"][0]["source"] == "March"


def test_list_inflows_invalid_month(client):
    resp = client.get("/api/v1/inflows?month=2026-3")
    assert resp.status_code == 422
