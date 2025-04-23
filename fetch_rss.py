import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

from schemas import ParkingGarage, ParkingGarageResponse, ParkingGarageFilters
from pydantic import BaseModel, Field


def parse_description(description):
    """Parse the description field to extract status and available spots"""
    # Example format: "open / 172"
    parts = description.split(' / ')
    if len(parts) == 2:
        status = parts[0].strip()
        try:
            available_spots = int(parts[1].strip())
        except ValueError:
            available_spots = 0
        return status, available_spots
    return "unknown", 0

def extract_name(title):
    """Extract parking name from the title field"""
    # Example format: "Parkhaus Accu / Otto-Schütz-Weg"
    parts = title.split(' / ')
    if len(parts) == 2:
        return parts[0].strip()
    return title

def fetch_and_parse_rss() -> ParkingGarageResponse:
    """Fetch the RSS feed and parse the data"""
    url = "https://www.pls-zh.ch/plsFeed/rss"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching RSS feed: {response.status_code}")
            return ParkingGarageResponse(data=[], count=0)
        
        root = ET.fromstring(response.content)
        
        parking_data = []
        fetch_time = datetime.now()
        
        # Find all item elements in the RSS feed
        ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
        channel = root.find('channel')
        
        if channel is not None:
            for item in channel.findall('item'):
                title = item.find('title').text if item.find('title') is not None else ""
                description = item.find('description').text if item.find('description') is not None else ""
                dc_date = item.find('dc:date', ns).text if item.find('dc:date', ns) is not None else ""
                
                name = extract_name(title)
                status, available_spots = parse_description(description)
                
                # Parse the update time
                update_time = None
                if dc_date:
                    try:
                        update_time = datetime.strptime(dc_date, '%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                        update_time = fetch_time
                else:
                    update_time = fetch_time
                
                parking_data.append(
                    ParkingGarage(
                        name=name,
                        status=status,
                        available_spots=available_spots,
                        update_time=update_time,
                        fetch_time=fetch_time
                    )
                )
                
        return ParkingGarageResponse(
            data=parking_data,
            count=len(parking_data),
            timestamp=fetch_time
        )
    
    except Exception as e:
        print(f"Error processing the RSS feed: {e}")
        return ParkingGarageResponse(data=[], count=0)

def filter_parking_data(data: List[ParkingGarage], filters: ParkingGarageFilters) -> List[ParkingGarage]:
    """Filter parking data based on provided filters"""
    filtered_data = data
    
    if filters.name:
        filtered_data = [p for p in filtered_data if filters.name.lower() in p.name.lower()]
    
    if filters.status:
        filtered_data = [p for p in filtered_data if p.status.lower() == filters.status.lower()]
    
    if filters.min_spots is not None:
        filtered_data = [p for p in filtered_data if p.available_spots >= filters.min_spots]
    
    if filters.max_spots is not None:
        filtered_data = [p for p in filtered_data if p.available_spots <= filters.max_spots]
    
    return filtered_data

if __name__ == "__main__":
    print("Fetching and parsing RSS feed...")
    parking_data = fetch_and_parse_rss()
    if parking_data:
        print("Fetched and parsed RSS feed successfully.")
        for garage in parking_data.data:
            print(f"Name: {garage.name:^40} | Status: {garage.status:^7} | Available Spots: {garage.available_spots:^8} | Update Time: {garage.update_time} | Fetch Time: {garage.fetch_time}")
    else:
        print("No parking data found.")