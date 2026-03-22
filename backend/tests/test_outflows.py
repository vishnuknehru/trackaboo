"""Tests for /api/v1/outflows — CRUD + pagination + month filter."""


def _create_outflow(client, category_id, amount=500.0, date="2026-03-10", description=None):
    payload = {
        "categoryId": category_id,
        "amount": amount,
        "date": date,
        "description": description,
    }
    return client.post("/api/v1/outflows", json=payload)


# ── Create ───────────────────────────────────────────────────────────────────

def test_create_outflow_happy_path(client, seed_category):
    resp = _create_outflow(client, seed_category.id)
    assert resp.status_code == 201
    data = resp.json()
    assert data["amount"] == 500.0
    assert data["date"] == "2026-03-10"
    assert data["categoryId"] == seed_category.id
    assert "id" in data
    assert "createdAt" in data


def test_create_outflow_invalid_category(client):
    """Non-existent categoryId → 422 (FK violation)."""
    resp = _create_outflow(client, category_id=99999)
    assert resp.status_code == 422


def test_create_outflow_invalid_amount_zero(client, seed_category):
    resp = _create_outflow(client, seed_category.id, amount=0)
    assert resp.status_code == 422


def test_create_outflow_invalid_amount_negative(client, seed_category):
    resp = _create_outflow(client, seed_category.id, amount=-100.0)
    assert resp.status_code == 422


def test_create_outflow_invalid_date_format(client, seed_category):
    resp = _create_outflow(client, seed_category.id, date="10/03/2026")
    assert resp.status_code == 422


def test_create_outflow_missing_category(client):
    resp = client.post("/api/v1/outflows", json={"amount": 100.0, "date": "2026-03-01"})
    assert resp.status_code == 422


# ── Get ──────────────────────────────────────────────────────────────────────

def test_get_outflow_found(client, seed_category):
    outflow_id = _create_outflow(client, seed_category.id).json()["id"]
    resp = client.get(f"/api/v1/outflows/{outflow_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == outflow_id


def test_get_outflow_not_found(client):
    assert client.get("/api/v1/outflows/99999").status_code == 404


# ── Update ───────────────────────────────────────────────────────────────────

def test_patch_outflow_partial(client, seed_category):
    outflow_id = _create_outflow(client, seed_category.id, amount=200.0).json()["id"]
    resp = client.patch(f"/api/v1/outflows/{outflow_id}", json={"amount": 350.0})
    assert resp.status_code == 200
    data = resp.json()
    assert data["amount"] == 350.0
    assert data["categoryId"] == seed_category.id  # unchanged


def test_patch_outflow_not_found(client):
    assert client.patch("/api/v1/outflows/99999", json={"amount": 100.0}).status_code == 404


def test_patch_outflow_invalid_amount(client, seed_category):
    outflow_id = _create_outflow(client, seed_category.id).json()["id"]
    resp = client.patch(f"/api/v1/outflows/{outflow_id}", json={"amount": 0})
    assert resp.status_code == 422


# ── Delete ───────────────────────────────────────────────────────────────────

def test_delete_outflow_happy_path(client, seed_category):
    outflow_id = _create_outflow(client, seed_category.id).json()["id"]
    assert client.delete(f"/api/v1/outflows/{outflow_id}").status_code == 204
    assert client.get(f"/api/v1/outflows/{outflow_id}").status_code == 404


def test_delete_outflow_not_found(client):
    assert client.delete("/api/v1/outflows/99999").status_code == 404


# ── List / pagination ─────────────────────────────────────────────────────────

def test_list_outflows_empty(client):
    resp = client.get("/api/v1/outflows")
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["limit"] == 20


def test_list_outflows_pagination(client, seed_category):
    for i in range(5):
        _create_outflow(client, seed_category.id, amount=100.0 + i)

    resp = client.get("/api/v1/outflows?page=1&limit=3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["data"]) == 3

    resp2 = client.get("/api/v1/outflows?page=2&limit=3")
    assert len(resp2.json()["data"]) == 2


def test_list_outflows_month_filter(client, seed_category):
    _create_outflow(client, seed_category.id, amount=300.0, date="2026-03-05")
    _create_outflow(client, seed_category.id, amount=400.0, date="2026-04-10")

    resp = client.get("/api/v1/outflows?month=2026-03")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["data"][0]["amount"] == 300.0


def test_list_outflows_invalid_month(client):
    resp = client.get("/api/v1/outflows?month=26-03")
    assert resp.status_code == 422
