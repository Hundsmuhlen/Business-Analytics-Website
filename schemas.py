from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ParkingGarage(BaseModel):
    """Schema for a parking garage data item"""
    name: str = Field(..., description="Name of the parking garage")
    status: str = Field(..., description="Current status of the parking garage (e.g., 'open', 'closed')")
    available_spots: int = Field(..., description="Number of available parking spots")
    update_time: datetime = Field(..., description="Time when the parking data was last updated")
    fetch_time: datetime = Field(..., description="Time when the data was fetched from the source")

class ParkingGarageResponse(BaseModel):
    """Schema for a response containing a list of parking garages"""
    data: List[ParkingGarage] = Field(..., description="List of parking garage data items")
    count: int = Field(..., description="Total number of parking garages in the response")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the response")

class ParkingGarageFilters(BaseModel):
    """Schema for filtering parking garage data"""
    name: Optional[str] = Field(None, description="Filter by parking garage name")
    status: Optional[str] = Field(None, description="Filter by status (open/closed)")
    min_spots: Optional[int] = Field(None, description="Minimum number of available spots")
    max_spots: Optional[int] = Field(None, description="Maximum number of available spots")