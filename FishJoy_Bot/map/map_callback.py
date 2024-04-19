from bot.father_bot import bot
from bot.models import Spots
from map.map_main import get_map


@bot.callback_query_handler(func=lambda call: call.data.startswith('map'))
def handle_map(callback):
    spot_id = callback.data.split('_')[-1]
    spot_instance = Spots.objects.get(pk=spot_id)

    response = get_map(spot_instance.location)

    if response is not False:
        bot.send_location(callback.message.chat.id, *response)
    else:
        bot.send_message(callback.message.chat.id, "Unfortunately I can't find the location")
