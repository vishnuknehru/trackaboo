"""Tests for /api/v1/categories — CRUD + FK constraint."""

from app.models import Category, Outflow


# ── Helpers ──────────────────────────────────────────────────────────────────

def _create_cat(client, name="Housing", type_="outflow", color=None, description=None):
    return client.post(
        "/api/v1/categories",
        json={"name": name, "type": type_, "color": color, "description": description},
    )


# ── List ─────────────────────────────────────────────────────────────────────

def test_list_categories_empty(client):
    resp = client.get("/api/v1/categories")
    assert resp.status_code == 200
    assert resp.json() == {"data": []}


def test_list_categories_type_filter(client):
    _create_cat(client, name="Rent", type_="outflow")
    _create_cat(client, name="Salary", type_="inflow")

    resp = client.get("/api/v1/categories?type=inflow")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["name"] == "Salary"


def test_list_categories_invalid_type(client):
    resp = client.get("/api/v1/categories?type=badvalue")
    assert resp.status_code == 422


# ── Create ───────────────────────────────────────────────────────────────────

def test_create_category_happy_path(client):
    resp = _create_cat(client, name="Housing", type_="outflow", color="#4CAF50")
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Housing"
    assert data["type"] == "outflow"
    assert data["color"] == "#4CAF50"
    assert "id" in data
    assert "createdAt" in data
    assert "updatedAt" in data


def test_create_category_missing_name(client):
    resp = client.post("/api/v1/categories", json={"type": "outflow"})
    assert resp.status_code == 422


def test_create_category_invalid_type(client):
    resp = client.post("/api/v1/categories", json={"name": "X", "type": "invalid"})
    assert resp.status_code == 422


def test_create_category_nullable_fields(client):
    """color and description can be omitted."""
    resp = _create_cat(client, name="Misc")
    assert resp.status_code == 201
    data = resp.json()
    assert data["color"] is None
    assert data["description"] is None


# ── Get by ID ────────────────────────────────────────────────────────────────

def test_get_category_found(client):
    cat_id = _create_cat(client, name="Housing").json()["id"]
    resp = client.get(f"/api/v1/categories/{cat_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == cat_id


def test_get_category_not_found(client):
    resp = client.get("/api/v1/categories/99999")
    assert resp.status_code == 404


# ── Update ───────────────────────────────────────────────────────────────────

def test_patch_category_partial_update(client):
    cat_id = _create_cat(client, name="OldName", color="#111111").json()["id"]
    resp = client.patch(f"/api/v1/categories/{cat_id}", json={"name": "NewName"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "NewName"
    assert data["color"] == "#111111"  # unchanged


def test_patch_category_not_found(client):
    resp = client.patch("/api/v1/categories/99999", json={"name": "X"})
    assert resp.status_code == 404


def test_patch_category_invalid_type(client):
    cat_id = _create_cat(client).json()["id"]
    resp = client.patch(f"/api/v1/categories/{cat_id}", json={"type": "bad"})
    assert resp.status_code == 422


# ── Delete ───────────────────────────────────────────────────────────────────

def test_delete_category_happy_path(client):
    cat_id = _create_cat(client).json()["id"]
    resp = client.delete(f"/api/v1/categories/{cat_id}")
    assert resp.status_code == 204
    # Confirm gone
    assert client.get(f"/api/v1/categories/{cat_id}").status_code == 404


def test_delete_category_not_found(client):
    resp = client.delete("/api/v1/categories/99999")
    assert resp.status_code == 404


def test_delete_category_fk_conflict(client, db_session):
    """Deleting a category referenced by an outflow must return 409."""
    cat_id = _create_cat(client, name="Rent").json()["id"]

    db_session.add(Outflow(
        amount=1000.0,
        date="2026-03-01",
        category_id=cat_id,
        description=None,
        created_at="2026-03-01T00:00:00Z",
        updated_at="2026-03-01T00:00:00Z",
    ))
    db_session.commit()

    resp = client.delete(f"/api/v1/categories/{cat_id}")
    assert resp.status_code == 409
