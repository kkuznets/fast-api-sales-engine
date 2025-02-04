from datetime import datetime
from typing import Optional

from fastapi import Query

from app.models import SaleCategoriesURL


# Get category from query parameters in routes
def get_category(
    category: Optional[SaleCategoriesURL] = Query(
        None,
        title="Category",
        description="Filter by category",
        examples=[list(SaleCategoriesURL)[0].value],
    ),
) -> Optional[SaleCategoriesURL]:
    return category


# Get start date from query parameters in routes
def get_start_date(
    start_date: Optional[datetime] = Query(
        None,
        title="Start Date",
        description="Filter by start date or datetime",
        examples=["2025-02-03 15:00:00"],
    ),
) -> Optional[datetime]:
    return start_date


# Get end date from query parameters in routes
def get_end_date(
    end_date: Optional[datetime] = Query(
        None,
        title="End Date",
        description="Filter by end date or datetime",
        examples=["2025-02-03 15:00:00"],
    ),
) -> Optional[datetime]:
    return end_date
