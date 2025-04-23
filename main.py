from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn

from fetch_rss import fetch_and_parse_rss, filter_parking_data
from schemas import ParkingGarage, ParkingGarageFilters
from fastapi.responses import FileResponse
# from fetch_weather import get_weather_info
from srf_weather import get_current_weather, WeatherData

app = FastAPI(title="Parking Garage API")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/parking", response_model=List[ParkingGarage])
async def get_parking_data(
    name: Optional[str] = Query(None, description="Filter by name"),
    min_spots: Optional[int] = Query(None, description="Minimum available spots"),
    max_spots: Optional[int] = Query(None, description="Maximum available spots"),
    sort_by: Optional[str] = Query(None, description="Sort by field: name or available_spots"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc")
):
    # Fetch and parse the RSS data
    response = fetch_and_parse_rss()
    
    # Apply initial filter to only include open parking garages
    filters = ParkingGarageFilters(
        name=name,
        status="open",  # Only show open parking garages
        min_spots=min_spots,
        max_spots=max_spots
    )
    
    filtered_data = filter_parking_data(response.data, filters)
    
    # Sort the data if requested
    if sort_by == "name":
        filtered_data.sort(key=lambda x: x.name, reverse=(sort_order == "desc"))
    elif sort_by == "available_spots":
        filtered_data.sort(key=lambda x: x.available_spots, reverse=(sort_order == "desc"))
    
    return filtered_data

@app.get("/api/weather", response_model=WeatherData)
async def get_weather():
    """
    Get current weather information including type and temperature.
    """
    weather_data = get_current_weather()
    return weather_data  # Return the object directly, not the JSON string

@app.get("/")
async def root():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)