import requests
import datetime

from bot.father_bot import bot

from bot.passwords import OPEN_CAGE_DATA, OPEN_WEATHER_MAP


def weather(location):
    # API to find location to get weather data

    api_key = OPEN_CAGE_DATA
    url = f'https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}'

    response = requests.get(url).json()
    if response['total_results'] == 0:
        location = 'Kyiv Ukraine'

    result = response['results'][0]
    latitude = result['geometry']['lat']
    longitude = result['geometry']['lng']

    # API to get current weather on this location
    key = OPEN_WEATHER_MAP
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={key}&units=metric'

    params = {'q': location, 'appid': key, 'units': 'metric'}

    r = requests.get(url=url, params=params)
    if not r.status_code == 200:
        print('BBBBBBBBBBBBBBBBBBAAAAAAAAAAAAAAADDDDDDDDDDDDDDDDDDDDD')

    res = r.json()

    description = res['weather'][0]['description']
    temp = res['main']['temp']
    pressure = res['main']['pressure']
    humidity = res['main']['humidity']
    wind = res['wind']['speed']
    day = datetime.date.fromtimestamp(res['dt']).strftime('%B %d %Y %I %p')

    weather_message = f"Weather forecast for {location}:\n\n"\
                      f"Description: {description}\n"\
                      f"Temperature: {temp}°C\n"\
                      f"Day: {day}\n"\
                      f"Pressure: {pressure} hPa\n"\
                      f"Humidity: {humidity}%\n"\
                      f"Wind: {wind} m/s\n"

    return weather_message
