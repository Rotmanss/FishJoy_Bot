from bot.father_bot import bot


def print_best_visiting_route(message, knm_result, queryset):
    result = ''
    for loc in queryset:
        for key, value in loc.items():
            if key == 'photo':
                photo = f'{value}'
                continue
            elif key == 'location':
                coords = value
                value = "{:.1f}°, {:.1f}°".format(*eval(value))
            elif key == 'title':
                value = f'{value}'
            else:
                continue

            result += f'<b>{' '.join(word for word in key.capitalize().split('_'))}</b> : {value}\n'

        for distance, x_y in knm_result['all_distances_and_coords']:
            if ', '.join(map(str, x_y)) == coords:
                related_to_spot_distance = distance

        result += f'Distance from your place to this spot: {related_to_spot_distance:.1f} km'
        bot.send_photo(message.chat.id, photo, caption=result)
        result = ''
