from bot.father_bot import bot
from bot.models import Spots


@bot.callback_query_handler(func=lambda call: call.data.startswith('map'))
def handle_map(callback):
    spot_id = callback.data.split('_')[-1]
    spot_instance = Spots.objects.get(pk=spot_id)

    lat, lon = spot_instance.location.split(',')

    bot.send_location(callback.message.chat.id, lat, lon)
