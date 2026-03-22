from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OutflowCreate(BaseModel):
    amount: float = Field(..., gt=0)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    category_id: int = Field(..., alias="categoryId")
    description: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class OutflowUpdate(BaseModel):
    """All fields optional for PATCH."""

    amount: Optional[float] = Field(default=None, gt=0)
    date: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    category_id: Optional[int] = Field(default=None, alias="categoryId")
    description: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class OutflowOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    amount: float
    date: str
    category_id: int = Field(alias="categoryId")
    description: Optional[str]
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

    @classmethod
    def from_orm_row(cls, row: object) -> OutflowOut:
        return cls(
            id=row.id,  # type: ignore[attr-defined]
            amount=row.amount,  # type: ignore[attr-defined]
            date=row.date,  # type: ignore[attr-defined]
            categoryId=row.category_id,  # type: ignore[attr-defined]
            description=row.description,  # type: ignore[attr-defined]
            createdAt=row.created_at,  # type: ignore[attr-defined]
            updatedAt=row.updated_at,  # type: ignore[attr-defined]
        )


class PaginatedOutflows(BaseModel):
    data: list[OutflowOut]
    total: int
    page: int
    limit: int
