from datetime import datetime, timedelta
from meteostat import Point, Hourly

# Set time period to get the latest data (last 24 hours)
end = datetime.now()
start = end - timedelta(days=1)

location = Point(47.36667, 8.55, 408)  # Zurich, Switzerland

# Get the latest hourly data
data = Hourly(location, start, end)
data = data.fetch()

# Print the latest data
print("Latest weather data:")
print(data.tail(1))  # Just the most recent hour

