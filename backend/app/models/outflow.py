from __future__ import annotations

from typing import Optional

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Outflow(Base):
    __tablename__ = "outflows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    # Decision: category_id NOT NULL on outflows — the dashboard category breakdown
    # requires every outflow to belong to a category (use "Uncategorized" as default).
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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

    category: Mapped[Category] = relationship(  # type: ignore[name-defined]
        "Category", back_populates="outflows"
    )
