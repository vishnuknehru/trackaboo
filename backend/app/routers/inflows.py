from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inflow import Inflow
from app.schemas.inflow import InflowCreate, InflowOut, InflowUpdate, PaginatedInflows

router = APIRouter()

_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@router.get("/inflows", response_model=PaginatedInflows)
def list_inflows(
    month: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PaginatedInflows:
    if month is not None and not _MONTH_RE.match(month):
        raise HTTPException(status_code=422, detail={"error": "month must be YYYY-MM"})

    query = db.query(Inflow)
    if month is not None:
        query = query.filter(
            Inflow.date >= f"{month}-01",
            Inflow.date <= f"{month}-31",
        )

    total: int = query.count()
    offset = (page - 1) * limit
    rows = query.order_by(Inflow.date.desc(), Inflow.id.desc()).offset(offset).limit(limit).all()

    return PaginatedInflows(
        data=[InflowOut.from_orm_row(r) for r in rows],
        total=total,
        page=page,
        limit=limit,
    )


@router.post("/inflows", response_model=InflowOut, status_code=201)
def create_inflow(body: InflowCreate, db: Session = Depends(get_db)) -> InflowOut:
    now = _now_utc()
    row = Inflow(
        amount=body.amount,
        date=body.date,
        source=body.source,
        description=body.description,
        category_id=body.category_id,
        created_at=now,
        updated_at=now,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return InflowOut.from_orm_row(row)


@router.get("/inflows/{inflow_id}", response_model=InflowOut)
def get_inflow(inflow_id: int, db: Session = Depends(get_db)) -> InflowOut:
    row = db.query(Inflow).filter(Inflow.id == inflow_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Inflow not found"})
    return InflowOut.from_orm_row(row)


@router.patch("/inflows/{inflow_id}", response_model=InflowOut)
def update_inflow(
    inflow_id: int, body: InflowUpdate, db: Session = Depends(get_db)
) -> InflowOut:
    row = db.query(Inflow).filter(Inflow.id == inflow_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Inflow not found"})

    update_data = body.model_dump(exclude_unset=True)
    # Map aliased field name back to column name
    if "category_id" in update_data:
        row.category_id = update_data.pop("category_id")
    for field, value in update_data.items():
        setattr(row, field, value)
    row.updated_at = _now_utc()

    db.commit()
    db.refresh(row)
    return InflowOut.from_orm_row(row)


@router.delete("/inflows/{inflow_id}", status_code=204, response_model=None)
def delete_inflow(inflow_id: int, db: Session = Depends(get_db)) -> None:
    row = db.query(Inflow).filter(Inflow.id == inflow_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Inflow not found"})
    db.delete(row)
    db.commit()
