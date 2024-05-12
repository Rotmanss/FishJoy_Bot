from bot.father_bot import bot
from bot.models import Spots
from weather.weather_main import get_weather


@bot.callback_query_handler(func=lambda call: call.data.startswith('weather'))
def handle_weather(callback):
    spot_id = callback.data.split('_')[-1]
    spot_instance = Spots.objects.get(pk=spot_id)

    weather_forecast, weather_icon = get_weather(spot_instance.location)

    if weather_forecast and weather_icon:
        bot.send_photo(callback.message.chat.id, weather_icon, caption=weather_forecast)
    else:
        bot.send_message(callback.message.chat.id,
                         f"An error occurred while fetching weather data. Please try again. If error "
                         f"still active, write a message to administration by pressing \'Feedback\' "
                         f"button.")
