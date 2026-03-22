from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter()


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@router.get("/categories", response_model=dict)
def list_categories(
    type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    query = db.query(Category)
    if type is not None:
        if type not in ("outflow", "inflow", "any"):
            raise HTTPException(
                status_code=422,
                detail={"error": "type must be one of: outflow, inflow, any"},
            )
        query = query.filter(Category.type == type)
    rows = query.order_by(Category.id).all()
    return {"data": [CategoryOut.from_orm_row(r) for r in rows]}


@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(body: CategoryCreate, db: Session = Depends(get_db)) -> CategoryOut:
    now = _now_utc()
    cat = Category(
        name=body.name,
        type=body.type,
        color=body.color,
        description=body.description,
        created_at=now,
        updated_at=now,
    )
    db.add(cat)
    try:
        db.commit()
        db.refresh(cat)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})
    return CategoryOut.from_orm_row(cat)


@router.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryOut:
    cat = db.query(Category).filter(Category.id == category_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail={"error": "Category not found"})
    return CategoryOut.from_orm_row(cat)


@router.patch("/categories/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int, body: CategoryUpdate, db: Session = Depends(get_db)
) -> CategoryOut:
    cat = db.query(Category).filter(Category.id == category_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail={"error": "Category not found"})

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cat, field, value)
    cat.updated_at = _now_utc()

    db.commit()
    db.refresh(cat)
    return CategoryOut.from_orm_row(cat)


@router.delete("/categories/{category_id}", status_code=204, response_model=None)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> None:
    cat = db.query(Category).filter(Category.id == category_id).first()
    if cat is None:
        raise HTTPException(status_code=404, detail={"error": "Category not found"})

    try:
        db.delete(cat)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        if "FOREIGN KEY constraint failed" in str(exc):
            raise HTTPException(
                status_code=409,
                detail={"error": "Category is referenced by existing outflows"},
            )
        raise HTTPException(status_code=500, detail={"error": "Internal server error"})
