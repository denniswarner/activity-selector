"""
Data models for the Activity Selector application.
"""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class PriceLevel(str, Enum):
    """Price level enumeration for activities."""
    FREE = "Free"
    LOW = "$"
    MEDIUM = "$$"
    HIGH = "$$$"
    LUXURY = "$$$$"


class Activity(BaseModel):
    """Model representing an activity."""
    name: str = Field(..., description="Name of the activity")
    description: Optional[str] = Field(None, description="Description of the activity")
    price_level: PriceLevel = Field(..., description="Price level of the activity")
    location: Optional[str] = Field(None, description="Location of the activity")
    category: str = Field(..., description="Category of the activity")
    address: Optional[str] = Field(None, description="Full address of the activity")
    phone: Optional[str] = Field(None, description="Phone number of the activity")
    url: Optional[str] = Field(None, description="Website or menu URL for the activity")
    notes: Optional[str] = Field(None, description="Personal notes, tips, or observations about the activity")
    last_visit_date: Optional[str] = Field(None, description="Date when this activity was last visited (YYYY-MM-DD format)")
    past_orders: Optional[List[str]] = Field(None, description="List of past orders (for restaurants)")
    last_bill_price: Optional[float] = Field(None, description="Last bill amount (for restaurants)")
    
    model_config = {
        "use_enum_values": True
    }


class Category(BaseModel):
    """Model representing an activity category."""
    name: str = Field(..., description="Name of the category")
    description: Optional[str] = Field(None, description="Description of the category")
    sheet_name: str = Field(..., description="Corresponding Google Sheets worksheet name")


class ActivityRequest(BaseModel):
    """Model for activity suggestion requests."""
    category: str = Field(..., description="Selected category")
    price_level: Optional[PriceLevel] = Field(None, description="Selected price level")
    limit: Optional[int] = Field(5, ge=1, le=20, description="Number of suggestions to return")


class ActivityResponse(BaseModel):
    """Model for activity suggestion responses."""
    activities: List[Activity] = Field(..., description="List of suggested activities")
    total_found: int = Field(..., description="Total number of activities found")
    category: str = Field(..., description="Category that was searched")
    price_level: Optional[PriceLevel] = Field(None, description="Price level that was filtered")


class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information") 