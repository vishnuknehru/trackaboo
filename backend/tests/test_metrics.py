"""Tests for GET /api/v1/metrics?month=YYYY-MM"""

from app.models import Category, Inflow, Outflow


def _add_category(db, name="Food", type_="outflow", color="#FF0000"):
    cat = Category(
        name=name,
        type=type_,
        color=color,
        description=None,
        created_at="2026-03-01T00:00:00Z",
        updated_at="2026-03-01T00:00:00Z",
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def test_metrics_empty_month(client):
    """No data for the month → all zeros, empty breakdown."""
    resp = client.get("/api/v1/metrics?month=2025-01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["month"] == "2025-01"
    assert data["totalInflow"] == 0.0
    assert data["totalOutflow"] == 0.0
    assert data["netFlow"] == 0.0
    assert data["categoryBreakdown"] == []


def test_metrics_with_data(client, db_session):
    """Happy path: inflows + outflows in range."""
    cat = _add_category(db_session)

    db_session.add(Inflow(
        amount=5000.0, date="2026-03-15", source="Salary", description=None,
        category_id=None, created_at="2026-03-15T00:00:00Z", updated_at="2026-03-15T00:00:00Z",
    ))
    db_session.add(Outflow(
        amount=1200.0, date="2026-03-10", category_id=cat.id, description="Rent",
        created_at="2026-03-10T00:00:00Z", updated_at="2026-03-10T00:00:00Z",
    ))
    db_session.add(Outflow(
        amount=800.0, date="2026-03-20", category_id=cat.id, description="Groceries",
        created_at="2026-03-20T00:00:00Z", updated_at="2026-03-20T00:00:00Z",
    ))
    db_session.commit()

    resp = client.get("/api/v1/metrics?month=2026-03")
    assert resp.status_code == 200
    data = resp.json()

    assert data["totalInflow"] == 5000.0
    assert data["totalOutflow"] == 2000.0
    assert data["netFlow"] == 3000.0
    assert len(data["categoryBreakdown"]) == 1
    bd = data["categoryBreakdown"][0]
    assert bd["categoryId"] == cat.id
    assert bd["categoryName"] == "Food"
    assert bd["amount"] == 2000.0
    assert bd["percentage"] == 100.0


def test_metrics_excludes_other_months(client, db_session):
    """Transactions outside the month should not be counted."""
    cat = _add_category(db_session)
    db_session.add(Inflow(
        amount=3000.0, date="2026-02-28", source="Bonus", description=None,
        category_id=None, created_at="2026-02-28T00:00:00Z", updated_at="2026-02-28T00:00:00Z",
    ))
    db_session.add(Outflow(
        amount=500.0, date="2026-02-10", category_id=cat.id, description=None,
        created_at="2026-02-10T00:00:00Z", updated_at="2026-02-10T00:00:00Z",
    ))
    db_session.commit()

    resp = client.get("/api/v1/metrics?month=2026-03")
    assert resp.status_code == 200
    data = resp.json()
    assert data["totalInflow"] == 0.0
    assert data["totalOutflow"] == 0.0


def test_metrics_invalid_month_format(client):
    """Bad month param → 422."""
    resp = client.get("/api/v1/metrics?month=2026-3")
    assert resp.status_code == 422


def test_metrics_missing_month(client):
    """Missing month param → 422."""
    resp = client.get("/api/v1/metrics")
    assert resp.status_code == 422


def test_metrics_percentage_calculation(client, db_session):
    """Verify percentage rounding to 2 decimals with two categories."""
    cat1 = _add_category(db_session, name="Housing", color="#111111")
    cat2 = _add_category(db_session, name="Food", color="#222222")
    db_session.add(Outflow(
        amount=700.0, date="2026-03-01", category_id=cat1.id, description=None,
        created_at="2026-03-01T00:00:00Z", updated_at="2026-03-01T00:00:00Z",
    ))
    db_session.add(Outflow(
        amount=300.0, date="2026-03-02", category_id=cat2.id, description=None,
        created_at="2026-03-02T00:00:00Z", updated_at="2026-03-02T00:00:00Z",
    ))
    db_session.commit()

    resp = client.get("/api/v1/metrics?month=2026-03")
    assert resp.status_code == 200
    data = resp.json()
    assert data["totalOutflow"] == 1000.0
    bd = {item["categoryName"]: item for item in data["categoryBreakdown"]}
    assert bd["Housing"]["percentage"] == 70.0
    assert bd["Food"]["percentage"] == 30.0
