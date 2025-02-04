from datetime import datetime
from typing import Optional

from sqlalchemy import String, cast
from sqlmodel.sql.expression import Select

from app.models import SaleCategoriesURL, Sale


# Build a query with optional filters
def build_query(
    base_query: Select,
    category: Optional[SaleCategoriesURL] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    order_by: Optional[str] = None,
) -> Select:
    if category:
        base_query = base_query.where(
            cast(Sale.CATEGORY, String).ilike(f"%{category.value}%")
        )
    if start_date:
        base_query = base_query.where(Sale.DATE_PAYMENT >= start_date)
    if end_date:
        base_query = base_query.where(Sale.DATE_PAYMENT <= end_date)
    if order_by:
        base_query = base_query.order_by(order_by)
    return base_query
