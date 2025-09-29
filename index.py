import requests
import pandas as pd
import json

# Your OpenWeatherMap API Key
API_KEY = "47bd84a2b0f4759542b6a925b368dcae"

# Base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Fetch weather data for a single city"""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # To get temperature in Celsius
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise error if response not 200
        data = response.json()

        return {
            "City": data["name"],
            "Country": data["sys"]["country"],
            "Temperature (°C)": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Humidity (%)": data["main"]["humidity"],
            "Wind Speed (m/s)": data["wind"]["speed"]
        }

    except requests.exceptions.RequestException as e:
        print(f" Network error for {city}: {e}")
    except KeyError:
        print(f" Could not fetch weather for {city}. Check city name or API key.")
    return None

def main():
    # Input multiple cities
    cities = input("Enter city names (comma-separated): ").split(",")

    results = []
    for city in cities:
        city = city.strip()
        weather = get_weather(city)
        if weather:
            results.append(weather)

    if results:
        # Save as JSON
        with open("weather_data.json", "w") as f:
            json.dump(results, f, indent=4)

        # Save as CSV
        df = pd.DataFrame(results)
        df.to_csv("weather_data.csv", index=False)

        print("\n Weather data saved to weather_data.json and weather_data.csv")
        print(df)  # Print neat table
    else:
        print(" No data fetched.")

if __name__ == "__main__":
    main()
