import requests

city = input("Enter city name: ")

try:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params,
        timeout=10
    )

    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if "results" not in geo_data or not geo_data["results"]:
        print("City not found.")

    else:
        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        print("\nWeather Information")
        print("-------------------")
        print(f"City: {location['name']}")
        print(f"Temperature: {current['temperature_2m']} °C")
        print(f"Humidity: {current['relative_humidity_2m']} %")
        print(f"Wind Speed: {current['wind_speed_10m']} km/h")

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")

except (KeyError, TypeError):
    print("Unexpected data received from the API.")