from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, func, select

from app.db import get_session
from app.dependencies import (
    get_category,
    get_end_date,
    get_start_date,
)
from app.helpers import build_query
from app.models import (
    CategorySummary,
    SaleCategoriesURL,
    Sale,
    SaleCreate,
)

router = APIRouter()


# Endpoint to get all sales with optional filters
@router.get(
    "/sales",
    summary="All sales",
)
async def sales(
    category: Optional[SaleCategoriesURL] = Depends(get_category),
    start_date: Optional[datetime] = Depends(get_start_date),
    end_date: Optional[datetime] = Depends(get_end_date),
    session: Session = Depends(get_session),
) -> list[Sale]:
    query = build_query(select(Sale), category, start_date, end_date)
    sales = session.exec(query).all()
    return sales


# Endpoint to get a sale by its id_oder (not unique)
@router.get(
    "/sales/{id_order}",
    summary="Sale(s) by their order ID",
)
async def get_sale_by_id(
    id_order: str = Path(
        ...,
        title="Sale ID",
        description="The unique identifier for the sale",
        example="34033734",
    ),
    session: Session = Depends(get_session),
) -> List[Sale]:
    query = select(Sale).where(Sale.ID_ORDER == id_order)
    result = session.exec(query).all()
    # Check if the sale exists or if result is empty
    if not result:
        raise HTTPException(status_code=404, detail="Sale not found")
    return result


# Endpoint to get a summary of top-3 categories within a date range
@router.get("/feedback", summary="Summary of the top-3 categories")
async def categories_summary(
    category: Optional[SaleCategoriesURL] = Depends(get_category),
    start_date: Optional[datetime] = Depends(get_start_date),
    end_date: Optional[datetime] = Depends(get_end_date),
    session: Session = Depends(get_session),
) -> List[CategorySummary]:
    base_query = select(
        Sale.CATEGORY.label("category"),
        func.count(Sale.ID).label("sales_count"),
        func.sum(Sale.REVENUE).label("total_revenue"),
    ).group_by(Sale.CATEGORY)
    query = build_query(
        base_query,
        category=category,
        start_date=start_date,
        end_date=end_date,
        order_by="sales_count",
    )
    results = session.exec(query).all()
    return [
        {
            "category": result.category,
            "sales_count": result.sales_count,
            "total_revenue": result.total_revenue,
        }
        for result in results[-3:]
    ]


# Endpoint to create a new sale
@router.post("/ingest", summary="Ingest a sale")
async def create_sale(
    sale_data: SaleCreate, session: Session = Depends(get_session)
) -> Sale:
    sale = Sale(
        **sale_data.model_dump(),
    )
    session.add(sale)
    session.commit()
    session.refresh(sale)
    return sale
