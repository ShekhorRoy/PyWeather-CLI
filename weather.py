import requests
import sys
import os
from pyfiglet import Figlet
from datetime import datetime

# --- CONFIGURATION ---
# IMPORTANT: Replace 'YOUR_API_KEY_HERE' with your actual API key from a service 
# like OpenWeatherMap, WeatherAPI, etc.
API_KEY = "YOUR_API_KEY_HERE" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather" 

# Set up text styling
class Color:
    """Class for terminal color codes."""
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Prints a styled banner using pyfiglet."""
    f = Figlet(font='slant')
    print(Color.CYAN + f.renderText('PyWeather') + Color.END)
    print(Color.YELLOW + "---------------------------------------------------" + Color.END)
    print(Color.GREEN + "A simple command-line weather viewer." + Color.END)
    print(Color.YELLOW + "---------------------------------------------------" + Color.END)

def get_weather_data(city):
    """
    Fetches weather data from the API for a given city.

    Args:
        city (str): The name of the city to query.

    Returns:
        dict: A dictionary containing the weather data, or None on failure.
    """
    if API_KEY == "YOUR_API_KEY_HERE":
        print(Color.RED + "\n[ERROR] Please replace 'YOUR_API_KEY_HERE' in weather_app.py with your actual API key." + Color.END)
        return None

    print(f"\n{Color.DARKCYAN}Searching for weather in {city}...{Color.END}")
    
    params = {
        'q': city,
        'appid': API_KEY,
        # Units can be 'metric' (Celsius) or 'imperial' (Fahrenheit)
        'units': 'metric' 
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # Check specific status codes for common API errors
        if response.status_code == 404:
            print(Color.RED + f"\n[ERROR] City not found: {city}" + Color.END)
            return None
        elif response.status_code == 401:
            print(Color.RED + "\n[ERROR] Invalid API Key. Please check your key configuration." + Color.END)
            return None

        return response.json()

    except requests.exceptions.HTTPError as e:
        print(Color.RED + f"\n[ERROR] HTTP Error occurred: {e}" + Color.END)
    except requests.exceptions.ConnectionError:
        print(Color.RED + "\n[ERROR] Connection Error. Please check your network and API endpoint." + Color.END)
    except requests.exceptions.Timeout:
        print(Color.RED + "\n[ERROR] Request timed out." + Color.END)
    except requests.exceptions.RequestException as e:
        print(Color.RED + f"\n[ERROR] An unexpected error occurred: {e}" + Color.END)

    return None

def display_weather(data):
    """
    Prints the formatted weather data to the console.

    Args:
        data (dict): The JSON weather data dictionary.
    """
    try:
        # Extract necessary fields
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        description = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']
        
        # Convert timestamps for sunrise/sunset (OpenWeatherMap provides UTC timestamps)
        sunrise_ts = data['sys']['sunrise']
        sunset_ts = data['sys']['sunset']
        
        # Format times
        sunrise_time = datetime.fromtimestamp(sunrise_ts).strftime('%H:%M:%S')
        sunset_time = datetime.fromtimestamp(sunset_ts).strftime('%H:%M:%S')

        # Print result
        print(Color.YELLOW + "\n==============================================" + Color.END)
        print(f"{Color.BOLD}{city}, {country}{Color.END}")
        print(Color.YELLOW + "==============================================" + Color.END)
        
        print(f"🌡️  {Color.BLUE}Temperature:{Color.END} {temp:.1f}°C (Feels like: {feels_like:.1f}°C)")
        print(f"☁️  {Color.BLUE}Condition:  {Color.END} {description}")
        print(f"💧  {Color.BLUE}Humidity:   {Color.END} {humidity}%")
        print(f"💨  {Color.BLUE}Wind Speed: {Color.END} {wind_speed} m/s")
        print(f"⏱️  {Color.BLUE}Pressure:   {Color.END} {pressure} hPa")
        print(f"🌅  {Color.BLUE}Sunrise:    {Color.END} {sunrise_time}")
        print(f"🌇  {Color.BLUE}Sunset:     {Color.END} {sunset_time}")
        
        print(Color.YELLOW + "==============================================" + Color.END)

    except KeyError as e:
        print(Color.RED + f"[ERROR] Data structure error. Missing key: {e}" + Color.END)
    except Exception as e:
        print(Color.RED + f"[ERROR] An error occurred while displaying data: {e}" + Color.END)


def main():
    """Main function to parse arguments and run the application."""
    print_banner()

    if len(sys.argv) != 2:
        print(f"\n{Color.BOLD}Usage:{Color.END} python {sys.argv[0]} <city_name>")
        print(f"{Color.BOLD}Example:{Color.END} python {sys.argv[0]} \"London, UK\"")
        sys.exit(1)

    city_name = sys.argv[1]
    
    weather_data = get_weather_data(city_name)
    
    if weather_data:
        display_weather(weather_data)

if __name__ == "__main__":
    main()