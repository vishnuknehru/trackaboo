from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: Literal["outflow", "inflow", "any"] = "outflow"
    color: Optional[str] = None
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    """All fields optional for PATCH."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    type: Optional[Literal["outflow", "inflow", "any"]] = None
    color: Optional[str] = None
    description: Optional[str] = None


class CategoryOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    name: str
    type: str
    color: Optional[str]
    description: Optional[str]
    # Decision: aliases expose camelCase to match the TypeScript frontend contract.
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

    @classmethod
    def from_orm_row(cls, row: object) -> CategoryOut:
        """Map ORM model (snake_case attrs) → camelCase output schema."""
        return cls(
            id=row.id,  # type: ignore[attr-defined]
            name=row.name,  # type: ignore[attr-defined]
            type=row.type,  # type: ignore[attr-defined]
            color=row.color,  # type: ignore[attr-defined]
            description=row.description,  # type: ignore[attr-defined]
            createdAt=row.created_at,  # type: ignore[attr-defined]
            updatedAt=row.updated_at,  # type: ignore[attr-defined]
        )
