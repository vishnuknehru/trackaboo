from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inflow import Inflow
from app.models.outflow import Outflow
from app.models.category import Category
from app.schemas.metrics import CategoryBreakdownItem, MonthlyMetricsOut

router = APIRouter()

_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


@router.get("/metrics", response_model=MonthlyMetricsOut)
def get_metrics(
    month: str = Query(..., description="Month in YYYY-MM format"),
    db: Session = Depends(get_db),
) -> MonthlyMetricsOut:
    if not _MONTH_RE.match(month):
        raise HTTPException(status_code=422, detail={"error": "month must be YYYY-MM"})

    # Decision: use 'YYYY-MM-01' / 'YYYY-MM-31' range — SQLite text dates sort
    # lexicographically so this covers all days without computing the true last day.
    date_start = f"{month}-01"
    date_end = f"{month}-31"

    # Total inflow for the month
    total_inflow_result = (
        db.query(func.sum(Inflow.amount))
        .filter(Inflow.date >= date_start, Inflow.date <= date_end)
        .scalar()
    )
    total_inflow: float = float(total_inflow_result or 0.0)

    # Outflow totals grouped by category
    rows = (
        db.query(
            func.sum(Outflow.amount).label("amount"),
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            Category.color.label("color"),
        )
        .join(Category, Outflow.category_id == Category.id)
        .filter(Outflow.date >= date_start, Outflow.date <= date_end)
        .group_by(Category.id)
        .all()
    )

    total_outflow: float = sum(float(r.amount) for r in rows)

    breakdown: list[CategoryBreakdownItem] = []
    for r in rows:
        pct = round(float(r.amount) / total_outflow * 100, 2) if total_outflow > 0 else 0.0
        breakdown.append(
            CategoryBreakdownItem(
                categoryId=r.category_id,
                categoryName=r.category_name,
                amount=float(r.amount),
                percentage=pct,
                color=r.color,
            )
        )

    return MonthlyMetricsOut(
        month=month,
        totalInflow=total_inflow,
        totalOutflow=total_outflow,
        netFlow=round(total_inflow - total_outflow, 10),
        categoryBreakdown=breakdown,
    )
