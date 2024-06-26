import functools

from best_visiting_route.build_graph import create_graph
from best_visiting_route.ant_colony_optimization import AntColonyOptimization
from best_visiting_route.controllers.print_best_visiting_route import print_best_visiting_route
from best_visiting_route.show_connections import show_connections

from bot.father_bot import bot

from best_visiting_route.k_nearest_neighbors import KNearestNeighbours
from bot.go_back import go_back
from bot.models import Spots

import matplotlib.pyplot as plt

from django.db.models import Case, When


@bot.callback_query_handler(func=lambda call: call.data.startswith('search_nearest_spots'))
def handle_search_nearest_spots(callback):
    bot.send_message(callback.message.chat.id, "How much nearest location do you want to find?\n"
                                               "To return to the main menu type x")

    bot.register_next_step_handler(callback.message, lambda m: process_k(m))


def process_k(message):
    if go_back(message):
        return

    k = message.text
    try:
        if int(k) > 100:
            sent = bot.send_message(message.chat.id,
                                    "Currently we support search for maximum 100 nearest locations to you."
                                    "Select number between 1 and 10")
            bot.register_next_step_handler(sent, functools.partial(process_k))
            return
    except ValueError:
        sent = bot.send_message(message.chat.id, 'You inputted data incorrectly. Try again.')
        bot.register_next_step_handler(sent, functools.partial(process_k))
        return

    bot.send_message(message.chat.id, "Send me your location using telegram")
    bot.register_next_step_handler(message, lambda m: process_location(m, k))


@bot.message_handler(content_types=['location'])
def process_location(message, k):
    if go_back(message):
        return
    try:
        latitude = message.location.latitude
        longitude = message.location.longitude

        bot.reply_to(message, f"Received location: Latitude {latitude}, Longitude {longitude}")
    except AttributeError:
        sent = bot.reply_to(message, "You didn't send location. Please try again.")
        bot.register_next_step_handler(sent, functools.partial(process_location, k=k))
        return

    # latitude = 54.352912
    # longitude = 18.550590

    locations = list(Spots.objects.all().values_list('location', flat=True))
    prepare_locations = [loc.split(',') for loc in locations]
    normalized_locations = [[float(pair.strip()) for pair in sublist] for sublist in prepare_locations]

    # If user is already on one of possible locations, it will be treated as start point
    start_location = [latitude, longitude]
    try:
        index = normalized_locations.index(start_location)
        start_location = [latitude + 0.001, longitude]
    except ValueError:
        pass

    clf = KNearestNeighbours(int(k))
    clf.fit(normalized_locations)
    knm_result = clf.predict(start_location)

    filtered_result = []
    for distance, coords in knm_result['all_distances_and_coords']:
        if distance in knm_result['top_distances']:
            x, y = coords
            filtered_result.append(f'{x}, {y}')

    filtered_locations = list(Spots.objects.filter(location__in=filtered_result).values())

    # Building graph and creating distances matrix
    data_for_graph = [start_location]
    for id_and_coord in filtered_locations:
        lat, lon = id_and_coord['location'].split(',')
        data_for_graph.append(tuple(map(float, (lat, lon))))
    distances_matrix = create_graph(data_for_graph)

    # Running ACO algorithm
    aco = AntColonyOptimization(distances_matrix, num_ants=10, num_iterations=1000)
    best_route = aco.run()

    sorted_locations = [data_for_graph[i] for i in best_route]
    locations = [f"{lat}, {lng}" for lat, lng in sorted_locations]

    # Show location connections on world map
    show_con = []
    for i, loc in enumerate(locations):
        lat, lon = loc.split(',')
        lat, lon = map(float, (lat, lon))
        show_con.append({'name': f'Visit {i}; {lat:.1f}, {lon:.1f}', 'lat': lat, 'lon': lon})

    # Prepare and print locations in telegram
    ordering = Case(*[When(location=loc, then=pos) for pos, loc in enumerate(locations)])
    result = list(Spots.objects.filter(location__in=locations).values().order_by(ordering))

    print_best_visiting_route(message, knm_result, result)
    bot.reply_to(message, f"These are top {len(result)} closest locations to your current position to visit.\n"
                          f"They were sorted in such a way that if you want to visit them all, you should start "
                          f"from the first one sent by bot and go to the last one respectively. "
                          f"From the last location you should go to your current place.\n")
    show_connections(show_con, message)

    # show_plot(knm_result, (latitude, longitude), normalized_locations)


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
