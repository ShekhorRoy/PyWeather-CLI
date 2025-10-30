PyWeather CLI
==============

A simple Python command-line app to fetch real-time weather data.

Features
--------
- Real-time weather: temperature, conditions, humidity
- Stylish terminal output using pyfiglet
- Handles errors: network issues, invalid city names, wrong API keys
- Easy to use via command-line arguments

Dependencies
------------
- requests – HTTP requests to fetch weather data
- pyfiglet – ASCII art banners in the terminal

Prerequisites
-------------
- Python 3.6+
- API Key from a weather service (e.g., OpenWeatherMap)

Setup
-----
1. Install dependencies:
   pip install requests pyfiglet

2. Add your API key in `weather_app.py`:
   API_KEY = "YOUR_API_KEY_HERE"

Usage
-----
python weather_app.py "City Name"

Examples:
python weather_app.py "Tokyo"
python weather_app.py "London, UK"
python weather_app.py "InvalidCity"

Contribution
------------
Fork, improve, and submit pull requests. Ideas:
- 5-day / 3-hour forecast
- Caching API responses
- Celsius/Fahrenheit toggle
- Text-to-speech reports
