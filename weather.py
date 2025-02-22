import requests
import geocoder

def get_weather():
    g = geocoder.ip('me')
    if not g.latlng:
        return "Failed to retrieve location data."
    
    lat, lon = g.latlng
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&humidity=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data["current_weather"]["temperature"]
        wind = weather_data["current_weather"]["windspeed"]
        condition = weather_data["current_weather"]["weathercode"]
        
        weather_map = {0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                       45: "Fog", 48: "Depositing rime fog", 51: "Drizzle: Light",
                       53: "Drizzle: Moderate", 55: "Drizzle: Dense", 61: "Rain: Slight",
                       63: "Rain: Moderate", 65: "Rain: Heavy", 80: "Showers: Slight",
                       81: "Showers: Moderate", 82: "Showers: Violent", 95: "Thunderstorm: Slight",
                       96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"}
        
        weather_desc = weather_map.get(condition, "Unknown condition")
        return f"{temp}°C, {wind} km/h wind, {weather_desc}."
    
    return "Weather data not available."
