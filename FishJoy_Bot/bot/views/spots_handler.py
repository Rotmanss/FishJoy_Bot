from bot.father_bot import bot
from bot.views.base_handler import Handler
from bot.models import Spots, SpotCategory

from django.contrib.auth.models import User
from telebot.async_telebot import types

from bot.main_menu_keyboard import main_menu_keyboard


class SpotsHandler(Handler):
    def __init__(self, message):
        self.message = message

    def get_all_records(self, current_user_id):
        result = ''
        photo = 'AgACAgIAAxkBAAPmZgp3cwABhLE4BMdIQaTVrttbKafQAALZ4zEbOEZQSGkjdNm_ZtTWAQADAgADcwADNAQ'
        for spot in self._get_from_db():
            for key, value in spot.items():
                if key == 'photo':
                    photo = f'{value}'
                    continue

                elif key == 'id':
                    id = value
                    continue

                elif key == 'time_create' or key == 'time_update':
                    value = value.strftime('%B %d, %Y %I:%M %p')

                elif key == 'spot_category_id':
                    spot_category_instance = SpotCategory.objects.get(pk=value)
                    value = f'{spot_category_instance.name} (id: {spot_category_instance.id})'

                elif key == 'max_depth':
                    value = f'{value} meters'

                elif key == 'average_rating':
                    value = f'{value:.1f}'

                elif key == 'location':
                    value = "{:.1f}°, {:.1f}°".format(*eval(value))

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                if key == 'user_id' and str(value) == str(User.objects.get(username=current_user_id).id):
                    edit = types.InlineKeyboardButton("Edit spot", callback_data=f"edit_spot_{id}")
                    delete = types.InlineKeyboardButton("Delete spot", callback_data=f"delete_spot_{id}")
                    evaluate = types.InlineKeyboardButton("Rating", callback_data=f"evaluate_{id}")
                    keyboard.add(edit, delete, evaluate)
                    continue
                elif key == 'user_id' and User.objects.filter(username=current_user_id).exists():
                    evaluate = types.InlineKeyboardButton("Rating", callback_data=f"evaluate_{id}")
                    keyboard.add(evaluate)
                    continue
                elif key == 'user_id':
                    continue

                result += f'<b>{' '.join(word for word in key.capitalize().split('_'))}</b> : {value}\n'

            weather = types.InlineKeyboardButton("Weather", callback_data=f"weather_{id}")
            map = types.InlineKeyboardButton("Map", callback_data=f"map_{id}")
            keyboard.add(weather, map)
            bot.send_photo(self.message.chat.id, photo, caption=result, reply_markup=keyboard)

            result = ''

    @staticmethod
    def _get_from_db():
        return list(Spots.objects.all().order_by('average_rating').values())

    def add_record(self, data):
        spot = Spots.objects.create(title=data['title'],
                                    location=data['location'],
                                    photo=data['photo'],
                                    max_depth=data['max_depth'],
                                    spot_category_id=data['spot_category'],
                                    user_id=User.objects.get(username=str(data['user_id'])).id,
                                    average_rating=3)
        spot.save()
        bot.send_message(self.message.chat.id, 'Spot was added successfully.')

    def edit_record(self, record_id, field, new_value, field_title):
        instance = Spots.objects.get(pk=record_id)
        setattr(instance, field, new_value)
        instance.save()
        bot.send_message(self.message.chat.id, f"{field_title} has been updated.",
                         reply_markup=main_menu_keyboard)

    def delete_record(self, record_id):
        try:
            spot_instance = Spots.objects.get(pk=record_id)
            spot_instance.delete()
            bot.send_message(self.message.chat.id, f"Selected record has been deleted!")

        except:
            bot.send_message(self.message.chat.id, 'You entered data incorrectly')
