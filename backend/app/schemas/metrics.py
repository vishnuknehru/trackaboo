from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryBreakdownItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category_id: int = Field(alias="categoryId")
    category_name: str = Field(alias="categoryName")
    amount: float
    percentage: float
    color: Optional[str]


class MonthlyMetricsOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    month: str
    total_inflow: float = Field(alias="totalInflow")
    total_outflow: float = Field(alias="totalOutflow")
    net_flow: float = Field(alias="netFlow")
    category_breakdown: List[CategoryBreakdownItem] = Field(alias="categoryBreakdown")
