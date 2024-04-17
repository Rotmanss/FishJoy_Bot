from bot.father_bot import bot
from bot.models import Spots
from weather.weather_main import weather


@bot.callback_query_handler(func=lambda call: call.data.startswith('weather'))
def handle_weather(callback):
    spot_id = callback.data.split('_')[-1]
    spot_instance = Spots.objects.get(pk=spot_id)

    bot.send_message(callback.message.chat.id, weather(spot_instance.location))
