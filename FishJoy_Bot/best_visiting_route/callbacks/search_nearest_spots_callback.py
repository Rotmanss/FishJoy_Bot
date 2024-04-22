from bot.father_bot import bot

from best_visiting_route.k_nearest_neighbors import KNearestNeighbours
from bot.models import Spots

import matplotlib.pyplot as plt


@bot.callback_query_handler(func=lambda call: call.data.startswith('search_nearest_spots'))
def handle_search_nearest_spots(callback):
    bot.send_message(callback.message.chat.id, "How much nearest location do you want to find?")

    bot.register_next_step_handler(callback.message, lambda m: process_k(m))


def process_k(message):
    k = message.text

    bot.send_message(message.chat.id, "Send me your location using telegram")
    bot.register_next_step_handler(message, lambda m: process_location(m, k))


# @bot.message_handler(content_types=['location'])
def process_location(message, k):
    latitude = 54.352908  # message.location.latitude
    longitude = 30.550569  # message.location.longitude

    bot.reply_to(message, f"Received location: Latitude {latitude}, Longitude {longitude}")

    locations = get_all_locations_coordinates()
    prepare_locations = [loc.split(',') for loc in locations]
    normalized_locations = [[float(coord.strip()) for coord in sublist] for sublist in prepare_locations]

    clf = KNearestNeighbours(int(k))
    clf.fit(normalized_locations)
    result = clf.predict((latitude, longitude))

    bot.reply_to(message, f"{result}")

    show_plot(result, (latitude, longitude), normalized_locations)


def show_plot(result, new_point, points):
    ax = plt.subplot()
    ax.grid(True, color='#323232')
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for distance, coords in result['all_distances_and_coords']:
        x, y = coords
        color = 'green' if distance in result['top_distances'] else 'red'
        ax.scatter(x, y, color=color, s=60)

    ax.scatter(new_point[0], new_point[1], color="#FF0000", marker='*', s=200, zorder=100)

    for point in points:
        ax.plot([new_point[0], point[0]], [new_point[1], point[1]], color='white', linestyle='--', linewidth=1)

    plt.show()


def get_all_locations_coordinates():
    return list(Spots.objects.all().values_list('location', flat=True))
