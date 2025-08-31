import pandas as pd
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

city = "Arboga"
lat = 59.39387
lon = 15.83917
api_key = os.getenv("OPENWEATHER_API_KEY")

# Get hourly forecast including temp and feels_like
url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=daily,minutely,current&appid={api_key}"
response = requests.get(url)
data = response.json()

# Debug: check keys
print("Keys in API response:", data.keys())

# Extract rain forecasts with temp and feels_like
rain_forecasts = []
for forecast in data.get("hourly", [])[:5]:
    timestamp = forecast["dt"]
    rain_volume = forecast.get("rain", {}).get("1h", 0)
    temp_c = round(forecast.get("temp", 0) - 273.15, 1)
    feels_like_c = round(forecast.get("feels_like", 0) - 273.15, 1)
    
    rain_forecasts.append({
        "timestamp": timestamp,
        "volume": rain_volume,
        "time_str": datetime.fromtimestamp(timestamp).strftime("%H:%M"),
        "date_str": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d"),
        "temp_C": temp_c,
        "feels_like_C": feels_like_c
    })

# Create DataFrame
df = pd.DataFrame(rain_forecasts)

# Debug: inspect
print(df.head())

# Save to Excel
df.to_excel(f"{city}_weather.xlsx", index=False)
print(f"Excel file saved: {city}_weather.xlsx")