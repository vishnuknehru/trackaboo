from __future__ import annotations

from typing import Optional

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Inflow(Base):
    __tablename__ = "inflows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Decision: category_id nullable on inflows — income is often uncategorised in v1.
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default="(strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))",
    )
    updated_at: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default="(strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))",
    )

    category: Mapped[Optional[Category]] = relationship(  # type: ignore[name-defined]
        "Category", back_populates="inflows"
    )
