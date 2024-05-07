
# TODO add connections many to many
# TODO handle how much records user can get at once. For example they can be sorted by rating or other fields

import datetime
from bot.passwords import OPEN_CAGE_DATA, OPEN_WEATHER_MAP
import requests
from PIL import Image
from io import BytesIO


def get_weather(location):
    api_key = OPEN_CAGE_DATA
    lat, lon = location.split(',')
    url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}'

    response = requests.get(url).json()
    if response['total_results'] == 0:
        location = 'Kyiv Ukraine'

    result = response['results'][0]
    latitude = result['geometry']['lat']
    longitude = result['geometry']['lng']

    # API to get current weather on this location
    key = OPEN_WEATHER_MAP
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={key}&units=metric'

    params = {'appid': key, 'units': 'metric'}

    r = requests.get(url=url, params=params)
    if not r.status_code == 200:
        return None, None

    data = r.json()

    description = data['weather'][0]['description']
    temperature = data['main']['temp']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    day = datetime.date.fromtimestamp(data['dt']).strftime('%B %d %Y %I %p')
    icon_code = data['weather'][0]['icon']
    icon_url = f'http://openweathermap.org/img/wn/{icon_code}.png'

    # Fetch the weather icon
    icon_response = requests.get(icon_url)
    icon_image = Image.open(BytesIO(icon_response.content))

    forecast_message = f"Weather forecast:\n\n"\
                       f"Description: {description}\n"\
                       f"Temperature: {temperature}°C\n"\
                       f"Day: {day}\n"\
                       f"Pressure: {pressure} hPa\n"\
                       f"Humidity: {humidity}%\n"\
                       f"Wind: {wind_speed} m/s\n"

    return forecast_message, icon_image
