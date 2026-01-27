import httpx
from ...helpers.responses import success_response, error_response
import os

async def get_today_weather(lat: float, lon: float):
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url)
            
            if response.status_code == 404:
                return error_response(
                    message="Location not found"
                )
            elif response.status_code == 401:
                return error_response(
                    message="Invalid API key"
                )
            elif response.status_code != 200:
                return error_response(
                    message=f"Weather API error: {response.status_code}"
                )
            
            weather_data = response.json()
            
            processed_data = {
                "city": weather_data["name"],
                "country": weather_data["sys"]["country"],
                "latitude": weather_data["coord"]["lat"],
                "longitude": weather_data["coord"]["lon"],
                "temperature": weather_data["main"]["temp"],
                "feels_like": weather_data["main"]["feels_like"],
                "humidity": weather_data["main"]["humidity"],
                "pressure": weather_data["main"]["pressure"],
                "description": weather_data["weather"][0]["description"],
                "wind_speed": weather_data["wind"]["speed"],
                "wind_direction": weather_data["wind"].get("deg", 0),
                "visibility": weather_data.get("visibility", 0) / 1000,
                "timestamp": weather_data["dt"]
            }
            
            return success_response(
                message="Weather data retrieved successfully",
                data=processed_data
            )
    
    except httpx.RequestError:
        return error_response(
            message="Failed to connect to weather service"
        )
    except Exception as e:
        print(f"Error getting weather data: {str(e)}")
        return error_response(
            message=f"Failed to retrieve weather data: {str(e)}"
        )
