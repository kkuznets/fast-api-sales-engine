from datetime import datetime
from enum import Enum

from sqlmodel import Field, Column, SQLModel, TIMESTAMP, String


# Model for the category choices in the query parameters
class SaleCategoriesURL(str, Enum):
    CLOTHING = "clothing"
    SHOES = "shoes"
    ACCESSORIES = "accessories"
    JEWELLERY = "jewellery"
    BAGS = "bags"
    DESIGN_AND_DECORATION = "design_and_decoration"
    BOYS = "boys"
    GIRLS = "girls"
    SPORT_AND_LEISURE = "sport_and_leisure"
    HIGH_TECH = "high_tech"
    ART_AND_CULTURE = "art_and_culture"
    PET_ACCESSORIES = "pet_accessories"


# Model for the category choices in the database
class SaleCategories(str, Enum):
    CLOTHING = "clothing"
    SHOES = "shoes"
    ACCESSORIES = "accessories"
    JEWELLERY = "jewellery"
    BAGS = "bags"
    DESIGN_AND_DECORATION = "design & decoration"
    BOYS = "boys"
    GIRLS = "girls"
    SPORT_AND_LEISURE = "sport & leisure"
    HIGH_TECH = "high-tech"
    ART_AND_CULTURE = "art & culture"
    PET_ACCESSORIES = "pet accessories"


# Model for the /categories-summary route response
class CategorySummary(SQLModel):
    category: str
    sales_count: int
    total_revenue: float

    class Config:
        json_schema_extra = {
            "example": {
                "category": "clothing",
                "sales_count": 5,
                "total_revenue": 150.00,
            }
        }


#  Model for the sale data. ID is automatically generated on creation
class SaleBase(SQLModel):
    ID_ORDER: str = Field(
        sa_column=Column(
            "ID_ORDER",
            String,
            unique=True,
            nullable=False,
        )
    )
    ID_PRODUCT: str
    ID_BUYER: str
    ID_SELLER: str
    ID_SELLER_COUNTRY: str
    ID_BUYER_COUNTRY: str

    DATE_PAYMENT: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=False),
            nullable=False,
        )
    )

    BRAND: str = Field(default=None, nullable=True)
    CATEGORY: SaleCategories = Field(default=None, nullable=True)
    REVENUE: float


# Don't need to include any additional fields to create a sale
class SaleCreate(SaleBase):
    pass


#  Table for the sale data with the ID included (for database queries)
class Sale(SaleBase, table=True):
    __tablename__ = "sales"
    ID: int = Field(default=None, primary_key=True)

    class Config:
        json_schema_extra = {
            "example": {
                "ID_ORDER": "34033734",
                "ID_PRODUCT": "13681706",
                "ID_BUYER": "9666775",
                "ID_SELLER": "6723223",
                "ID_SELLER_COUNTRY": "203",
                "ID_BUYER_COUNTRY": "170",
                "DATE_PAYMENT": "2021-01-07 0:09:24",
                "BRAND": "Dsquared2",
                "CATEGORY": "clothing",
                "REVENUE": "57.27456",
            }
        }


# Model and table for the country data with the ID included (for database queries)
class Country(SQLModel, table=True):
    ID_COUNTRY: str = Field(default=None, primary_key=True)
    COUNTRY_NAME: str
    CONTINENT: str = Field(default=None, nullable=True)

    class Config:
        json_schema_extra = {
            "example": {
                "ID_COUNTRY": "170",
                "COUNTRY_NAME": "France",
                "CONTINENT": "Europe",
            }
        }
