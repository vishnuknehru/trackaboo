from __future__ import annotations

from typing import List, Optional

from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("type IN ('outflow', 'inflow', 'any')", name="category_type_check"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    # Decision: type stored as TEXT with CHECK constraint mirroring the Drizzle schema.
    type: Mapped[str] = mapped_column(String, nullable=False, default="outflow")
    color: Mapped[Optional[str]] = mapped_column(String, nullable=True)
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

    # Relationships (lazy loaded; used for FK validation only)
    # Decision: passive_deletes=True on outflows tells SQLAlchemy NOT to nullify
    # the FK before the DELETE — instead let SQLite enforce the RESTRICT constraint.
    inflows: Mapped[List] = relationship("Inflow", back_populates="category", passive_deletes=True)
    outflows: Mapped[List] = relationship("Outflow", back_populates="category", passive_deletes=True)
