from django.shortcuts import render
import requests

def index(request):
    # API keys
    api_key_weather = "190198c7bdbefed0ee2b60e6a3a60f5a"  # Replace with your OpenWeatherMap API key
    api_key_unsplash = "DO5uiaiocmy3ozQ-st-BCYkf07NOztF4DT13MYXlbVk"  # Replace with your Unsplash API key

    # Default city
    city = request.GET.get('city', 'New York')

    # Fetch weather data from OpenWeatherMap
    url_weather = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_weather}&units=metric"
    response_weather = requests.get(url_weather)
    weather_data = response_weather.json()

    # Fetch background image from Unsplash based on the city
    url_unsplash = f"https://api.unsplash.com/photos/random?query={city}&client_id={api_key_unsplash}"
    response_unsplash = requests.get(url_unsplash)
    image_data = response_unsplash.json()

    # Debugging: Print the Unsplash API response
    # print("Unsplash API Response:", image_data)

    # Check if the Unsplash API returned a valid image
    if response_unsplash.status_code == 200 and "urls" in image_data:
        image_url = image_data["urls"]["regular"]  # Use the 'regular' size image
    else:
        image_url = None  # Fallback if no image is found

    # Handle weather data
    if weather_data.get("cod") != 200:
        context = {"error": "City not found!"}
    else:
        context = {
            "city": weather_data["name"],
            "temperature": weather_data["main"]["temp"],
            "weather": weather_data["weather"][0]["description"],
            "icon": weather_data["weather"][0]["icon"],
            "image_url": image_url,  # Background image URL
        }

    return render(request, "index.html", context)