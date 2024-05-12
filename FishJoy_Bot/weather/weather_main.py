# TODO handle how much records user can get at once. For example they can be sorted by rating or other fields

import datetime
import pytz

from bot.models import WeatherIcons
from bot.passwords import OPEN_CAGE_DATA, OPEN_WEATHER_MAP
import requests


def utc_to_european_time(utc_timestamp):
    utc_datetime = datetime.datetime.utcfromtimestamp(utc_timestamp)
    utc_timezone = pytz.timezone('UTC')

    # Localize UTC datetime object
    localized_utc_datetime = utc_timezone.localize(utc_datetime)

    # TODO to get user's location
    european_timezone = pytz.timezone('Europe/Warsaw')
    european_datetime = localized_utc_datetime.astimezone(european_timezone)

    return european_datetime


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
    day = utc_to_european_time(data['dt']).strftime('%B %d %Y %I %p')
    icon_code = data['weather'][0]['icon']

    icon = WeatherIcons.objects.get(icon_code=icon_code)
    forecast_message = f"Current weather:\n\n"\
                       f"Description: {description}\n"\
                       f"Temperature: {temperature}°C\n"\
                       f"Day: {day}\n"\
                       f"Pressure: {pressure} hPa\n"\
                       f"Humidity: {humidity}%\n"\
                       f"Wind: {wind_speed} m/s\n\n"

    # API to get weather forecast for multiple days on this location
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={key}&units=metric'

    r = requests.get(url=url, params=params)
    if not r.status_code == 200:
        return None, None

    data = r.json()

    for forecast in data['list'][:12:2]:
        description = forecast['weather'][0]['description']
        temperature = forecast['main']['temp']
        pressure = forecast['main']['pressure']
        humidity = forecast['main']['humidity']
        wind_speed = forecast['wind']['speed']
        day = utc_to_european_time(forecast['dt']).strftime('%B %d %Y %I %p')

        forecast_message += f"Weather forecast for {day}:\n\n" \
                            f"Description: {description}\n" \
                            f"Temperature: {temperature}°C\n" \
                            f"Pressure: {pressure} hPa\n" \
                            f"Humidity: {humidity}%\n" \
                            f"Wind: {wind_speed} m/s\n\n"

    return forecast_message, str(icon.icon_image)
