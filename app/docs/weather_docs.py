# Get Today's Weather Documentation
GET_TODAY_WEATHER_DOCS = {
    "summary": "Get Today's Weather",
    "description": """
    Get current weather information for specific coordinates using OpenWeatherMap API.
    
    **Process:**
    1. Query OpenWeatherMap API for current weather using coordinates
    2. Extract and format relevant weather data
    3. Return structured weather information
    
    **Parameters:**
    - lat: Latitude of the location (-90 to 90)
    - lon: Longitude of the location (-180 to 180)
    
    **Returns:**
    - Current temperature, humidity, pressure, wind conditions
    - Weather description and visibility
    - City and country information
    - Coordinates used for the query
    
    **Note:**
    - Requires valid OpenWeatherMap API key
    - Temperature in Celsius
    - Wind speed in m/s
    - Visibility in kilometers
    """,
    "responses": {
        200: {
            "description": "Weather data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Weather data retrieved successfully",
                        "data": {
                            "city": "London",
                            "country": "GB",
                            "latitude": 51.5074,
                            "longitude": -0.1278,
                            "temperature": 15.5,
                            "feels_like": 14.2,
                            "humidity": 72,
                            "pressure": 1013,
                            "description": "partly cloudy",
                            "wind_speed": 5.2,
                            "wind_direction": 230,
                            "visibility": 10.0,
                            "timestamp": 1706198400
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad request - Invalid coordinates or API error",
            "content": {
                "application/json": {
                    "examples": {
                        "location_not_found": {
                            "summary": "Location not found",
                            "value": {
                                "status": "error",
                                "message": "Location not found"
                            }
                        },
                        "invalid_api_key": {
                            "summary": "Invalid API key",
                            "value": {
                                "status": "error",
                                "message": "Invalid API key"
                            }
                        }
                    }
                }
            }
        },
        500: {
            "description": "Internal server error - Weather service unavailable",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Failed to connect to weather service"
                    }
                }
            }
        }
    }
}
