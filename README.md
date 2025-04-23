# Zurich Parking Availability Project

This project provides real-time information about parking garage availability in Zurich, along with current weather data from SRF. It's a group project developed for the ETH Business Analytics course.

## Features

- Real-time parking garage availability data for the city of Zurich
- Current weather information for Zurich fetched from the SRF Meteo API
- Web interface to display parking and weather data
- Future implementation: ML model to predict parking spot availability

## Getting Started

### Prerequisites

Make sure you have Python installed on your system.

### Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Simply run the main.py file:

```bash
python main.py
```

The web application will be served at: http://localhost:8000

## Project Structure

- `main.py`: Main application entry point
- `fetch_rss.py`: Fetches parking data from Zurich city sources
- `srf_weather.py`: Retrieves weather data from SRF Meteo API
- `schemas.py`: Pydantic data models for the application
- `static/`: Contains static web files including index.html

## Data Sources

- Parking data: Zürich City parking garages
- Weather data: SRF Meteo API (data for Zurich coordinates: 47.3797, 8.5342)

## Future Development

This project will be extended with machine learning capabilities to predict parking spot availability based on historical data, weather conditions, and other factors.

## Contributors

ETH Zurich - Business Analytics Course Group Project

## License
MIT License

Copyright (c) 2025 ETH Zurich Business Analytics Group Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.