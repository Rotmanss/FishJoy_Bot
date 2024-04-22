import requests

from bot.passwords import OPEN_CAGE_DATA


def get_map(location):
    try:
        api_key = OPEN_CAGE_DATA
        # TODO Error handling
        lat, lon = location.split(',')
        url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}'

        response = requests.get(url).json()

        result = response['results'][0]

        latitude = result['geometry']['lat']
        longitude = result['geometry']['lng']

        print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ', latitude, longitude)

        return latitude, longitude
    except:
        return False
