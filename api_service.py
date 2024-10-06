import requests
import logging
from config import API_KEY, CITIES

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def fetch_weather_data(city):
    """Fetch weather data from Openweather"""
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"API Visit failure: {e}")
        return None
