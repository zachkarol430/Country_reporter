import os
import requests



def get_weather(city: str):
    """Fetch weather data for a given city."""
    API_KEY = os.getenv('OPENWEATHER_API_KEY')  # Get API key from environment variable
    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather for {city}: {response.status_code}")
        return None 
    

