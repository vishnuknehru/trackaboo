from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.outflow import Outflow
from app.schemas.outflow import OutflowCreate, OutflowOut, OutflowUpdate, PaginatedOutflows

router = APIRouter()

_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@router.get("/outflows", response_model=PaginatedOutflows)
def list_outflows(
    month: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PaginatedOutflows:
    if month is not None and not _MONTH_RE.match(month):
        raise HTTPException(status_code=422, detail={"error": "month must be YYYY-MM"})

    query = db.query(Outflow)
    if month is not None:
        query = query.filter(
            Outflow.date >= f"{month}-01",
            Outflow.date <= f"{month}-31",
        )

    total: int = query.count()
    offset = (page - 1) * limit
    rows = (
        query.order_by(Outflow.date.desc(), Outflow.id.desc()).offset(offset).limit(limit).all()
    )

    return PaginatedOutflows(
        data=[OutflowOut.from_orm_row(r) for r in rows],
        total=total,
        page=page,
        limit=limit,
    )


@router.post("/outflows", response_model=OutflowOut, status_code=201)
def create_outflow(body: OutflowCreate, db: Session = Depends(get_db)) -> OutflowOut:
    now = _now_utc()
    row = Outflow(
        amount=body.amount,
        date=body.date,
        category_id=body.category_id,
        description=body.description,
        created_at=now,
        updated_at=now,
    )
    db.add(row)
    try:
        db.commit()
        db.refresh(row)
    except IntegrityError as exc:
        db.rollback()
        if "FOREIGN KEY constraint failed" in str(exc):
            raise HTTPException(
                status_code=422,
                detail={"error": "category_id references a non-existent category"},
            )
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})
    return OutflowOut.from_orm_row(row)


@router.get("/outflows/{outflow_id}", response_model=OutflowOut)
def get_outflow(outflow_id: int, db: Session = Depends(get_db)) -> OutflowOut:
    row = db.query(Outflow).filter(Outflow.id == outflow_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Outflow not found"})
    return OutflowOut.from_orm_row(row)


@router.patch("/outflows/{outflow_id}", response_model=OutflowOut)
def update_outflow(
    outflow_id: int, body: OutflowUpdate, db: Session = Depends(get_db)
) -> OutflowOut:
    row = db.query(Outflow).filter(Outflow.id == outflow_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Outflow not found"})

    update_data = body.model_dump(exclude_unset=True)
    if "category_id" in update_data:
        row.category_id = update_data.pop("category_id")
    for field, value in update_data.items():
        setattr(row, field, value)
    row.updated_at = _now_utc()

    try:
        db.commit()
        db.refresh(row)
    except IntegrityError as exc:
        db.rollback()
        if "FOREIGN KEY constraint failed" in str(exc):
            raise HTTPException(
                status_code=422,
                detail={"error": "category_id references a non-existent category"},
            )
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})

    return OutflowOut.from_orm_row(row)


@router.delete("/outflows/{outflow_id}", status_code=204, response_model=None)
def delete_outflow(outflow_id: int, db: Session = Depends(get_db)) -> None:
    row = db.query(Outflow).filter(Outflow.id == outflow_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Outflow not found"})
    db.delete(row)
    db.commit()
