from flask import Flask, render_template
from dotenv import load_dotenv
from time import time
from datetime import datetime
import requests
import os




cache = {"data": None, "timestamp": 0}

load_dotenv()

app = Flask(__name__)

def get_weather_data(city, lat, lon):
    date_str = datetime.now().strftime("%Y-%m-%d")

    if cache["data"] and time() - cache["timestamp"] < 600:  # 10 minutes
        return cache["data"]

    api_key = os.getenv("OPENWEATHER_API_KEY")  
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,alerts&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data.get("current", {})
        temperature_celsius = data["current"]["temp"] - 273.15
        feels_like_celsius = data["current"]["feels_like"] - 273.15
        humidity = data["current"]["humidity"]
        description = data["current"]["weather"][0]["description"]
        icon = data["current"]["weather"][0]["icon"]

        # Extract next 5 hourly forecasts
        rain_forecasts = []
        hourly_data = data.get("hourly", [])[:5]

        for forecast in hourly_data:
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

        # Pick first forecast for main display
        if rain_forecasts:
            forecast_datetime = f"{rain_forecasts[0]['date_str']}-{rain_forecasts[0]['time_str']}"
        else:
            forecast_datetime = "No forecast available"

        weather_info = {
            "city": city,
            "temperature": round(temperature_celsius, 1),
            "feels_like": round(feels_like_celsius, 1),
            "humidity": humidity,
            "description": description,
            "icon": icon,
            "rain_forecasts": rain_forecasts,
            "forecast_datetime": forecast_datetime
        }

        cache["data"] = weather_info
        cache["timestamp"] = time()
        return weather_info

    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None

@app.route("/")
def index():
    city = "Arboga"
    lat = 59.39387
    lon = 15.83917
    weather_data = get_weather_data(city, lat, lon)

    if weather_data:
       
       return render_template(
            "webb_app.html",
            weather_data=weather_data,
            lat=lat,
            lon=lon,
            current_date=datetime.now().strftime("%Y-%m-%d") 
        )
    else:
        return "Error fetching weather data."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)