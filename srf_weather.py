import requests
import json
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """
    Schema for weather data
    """
    temperature: float = Field(..., description="Temperature in Celsius")
    weather_type: str = Field(..., description="Weather type (e.g., clear, cloudy, rain)")
    time: str = Field(..., description="Time of the weather data in ISO format")


def get_current_weather(lat=47.3797, lon=8.5342) -> Optional[WeatherData]:
    """
    Fetch current weather data from SRF Meteo API
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        
    Returns:
        dict: Weather information including temperature and weather type
    """
    url = f"https://www.srf.ch/meteoapi/forecastpoint/{lat},{lon}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        # Get current time to find the closest hour data (as UTC timezone-aware)
        now = datetime.now(timezone.utc)
        
        # Check if 'hours' data is available
        if 'hours' in data:
            # Find the closest hour data to current time
            closest_hour = None
            min_time_diff = float('inf')
            
            for hour_data in data['hours']:
                hour_time = datetime.fromisoformat(hour_data['date_time'].replace('Z', '+00:00'))
                time_diff = abs((now - hour_time).total_seconds())
                
                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    closest_hour = hour_data
                    
            if closest_hour:
                # Get temperature
                temperature = closest_hour['TTT_C']
                
                # Determine weather type based on symbol code
                symbol_code = closest_hour['symbol_code']
                weather_type = determine_weather_type(symbol_code)
                
                return WeatherData(
                    temperature=temperature,
                    weather_type=weather_type,
                    time=closest_hour['date_time']
                )
                
                return {
                    'temperature': temperature,
                    'weather_type': weather_type,
                    'time': closest_hour['date_time']
                }
        
        # If hour data not available, use day data
        if 'days' in data and len(data['days']) > 0:
            today = data['days'][0]
            
            # Get temperature (average of min and max)
            temperature = (today['TX_C'] + today['TN_C']) / 2
            
            # Determine weather type based on symbol code
            symbol_code = today['symbol_code']
            weather_type = determine_weather_type(symbol_code)
            
            return WeatherData(
                temperature=temperature,
                weather_type=weather_type,
                time=today['date_time']
            )
            return {
                'temperature': temperature,
                'weather_type': weather_type,
                'time': today['date_time']
            }
            
        return {'error': 'No weather data found'}
        
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}
    except (json.JSONDecodeError, KeyError) as e:
        return {'error': f'Data parsing failed: {str(e)}'}

def determine_weather_type(symbol_code: int) -> str:
    """
    Determine weather type based on symbol code
    
    Args:
        symbol_code (int): Weather symbol code from SRF Meteo API
        
    Returns:
        str: Weather type description (clear, partly-cloudy, cloudy, rain, fog)
        
    https://developer.srgssr.ch/sites/default/files/inline-files/2023-05-10%20srf_meteo_api_commercial_eng_dok.pdf
    """
    # Convert to positive code for simplicity but keep track of day/night
    code = abs(symbol_code)
    
    # Map codes to weather types based on the documentation
    if code in [1, 10]:  # sonnig, ziemlich sonnig, klar, klare Abschnitte
        return "clear" 
    
    elif code in [3]:  # teils sonnig, Wolken: Sandsturm
        return "partly-cloudy"
    
    elif code in [19]:  # bedeckt
        return "cloudy"
    
    elif code in [20, 22, 4, 5, 25]:  # regnerisch, Schneeregen, Regenschauer, Regenschauer mit Gewitter
        return "rain"
    
    elif code in [21, 6, 8]:  # Schneefall, Schneeschauer, Schneeregenschauer
        # Note: Snow isn't in your target conditions, using "rain" as fallback
        return "rain"  
    
    elif code in [2, 17]:  # Nebelbänke, Nebel
        return "fog"
    
    else:
        # Default fallback
        return "cloudy"

if __name__ == "__main__":
    weather = get_current_weather()
    
    if 'error' in weather:
        print(f"Error: {weather['error']}")
    else:
        print(f"Current Weather for Zürich:")
        print(f"Temperature: {weather.temperature}°C")
        print(f"Conditions: {weather.weather_type}")
        print(f"Time: {weather.time}")