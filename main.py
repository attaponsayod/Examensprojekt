from dotenv import load_dotenv
import requests
import os
from html_generator import generate_html  # Import the function

load_dotenv()

def get_weather_data(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temperature_celsius = data["main"]["temp"] - 273.15

        weather_info = {
            "city": data["name"],
            "temperature": round(temperature_celsius, 1),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None

if __name__ == "__main__":
    import time

    city = "Stockholm"
    while True:
        weather_data = get_weather_data(city)
        if weather_data:
            generate_html(weather_data)  # Use the imported function
        time.sleep(3600)  # Wait for 1 hour (3600 seconds)
