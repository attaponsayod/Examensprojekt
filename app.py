from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import os
from time import time

cache = {"data": None, "timestamp": 0}

load_dotenv()

app = Flask(__name__)

def get_weather_data(city, lat, lon):
    if cache["data"] and time() - cache["timestamp"] < 600:  # 10 minutes
        return cache["data"]

    api_key = os.getenv("OPENWEATHER_API_KEY")  
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,daily&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temperature_celsius = data["current"]["temp"] - 273.15
        humidity = data["current"]["humidity"]
        description = data["current"]["weather"][0]["description"]
        icon = data["current"]["weather"][0]["icon"]

        # Extract rain forecast from the next few hours (if available)
        rain_forecasts = []
        if "hourly" in data:
            for forecast in data["hourly"][:5]:  # Check the next 5 hours
                if "rain" in forecast:
                    timestamp = forecast["dt"]
                    rain_volume = forecast["rain"].get("1h", 0)  # Rain volume in the next 1 hour
                    rain_forecasts.append({"timestamp": timestamp, "volume": rain_volume})


        weather_info = {
            "city": city,
            "temperature": round(temperature_celsius, 1),
            "humidity": humidity,
            "description": description,
             "icon": icon, 
            "rain_forecasts": rain_forecasts        
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
        return render_template("webb_app.html", weather_data=weather_data, lat=lat, lon=lon)
    else:
        return "Error fetching weather data."

if __name__ == "__main__":
    app.run(debug=True)