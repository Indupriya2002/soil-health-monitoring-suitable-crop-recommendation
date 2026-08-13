import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITY = "Rourkela"


def get_weather():
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)

    return temperature, humidity, rainfall


if __name__ == "__main__":
    temp, hum, rain = get_weather()

    print("Weather data fetched successfully")
    print(f"Temperature : {temp} °C")
    print(f"Humidity    : {hum} %")
    print(f"Rainfall    : {rain} mm (last 1 hour)")
