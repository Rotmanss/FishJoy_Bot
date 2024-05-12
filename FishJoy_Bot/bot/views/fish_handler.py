from bot.father_bot import bot
from bot.views.base_handler import Handler
from bot.models import Fish, FishCategory

from django.contrib.auth.models import User
from telebot.async_telebot import types

from bot.main_menu_keyboard import main_menu_keyboard


class FishHandler(Handler):
    def __init__(self, message):
        self.message = message

    def get_all_records(self, current_user_id):
        result = ''
        photo = 'AgACAgIAAxkBAAPmZgp3cwABhLE4BMdIQaTVrttbKafQAALZ4zEbOEZQSGkjdNm_ZtTWAQADAgADcwADNAQ'
        for fish in self._get_from_db():
            for key, value in fish.items():
                if key == 'photo':
                    photo = f'{value}'
                    continue

                elif key == 'id':
                    id = value
                    continue

                elif key == 'time_create' or key == 'time_update':
                    value = value.strftime('%B %d, %Y %I:%M %p')

                elif key == 'fish_category_id':
                    fish_category_instance = FishCategory.objects.get(pk=value)
                    value = f'{fish_category_instance.name} (id: {fish_category_instance.id})'

                elif key == 'average_weight':
                    value = f'{value} kg'

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                if key == 'user_id' and str(value) == str(User.objects.get(username=current_user_id).id):
                    edit = types.InlineKeyboardButton("Edit fish", callback_data=f"edit_fish_{id}")
                    delete = types.InlineKeyboardButton("Delete fish", callback_data=f"delete_fish_{id}")
                    keyboard.add(edit, delete)
                    continue
                elif key == 'user_id':
                    continue

                result += f'<b>{' '.join(word for word in key.capitalize().split('_'))}</b> : {value}\n'

            bot.send_photo(self.message.chat.id, photo, caption=result, reply_markup=keyboard)

            result = ''

    @staticmethod
    def _get_from_db():
        return list(Fish.objects.all().values())

    def add_record(self, data):
        fish = Fish.objects.create(name=data['name'],
                                   photo=data['photo'],
                                   average_weight=data['average_weight'],
                                   user_id=User.objects.get(username=str(data['user_id'])).id,
                                   fish_category_id=data['fish_category'],)
        fish.save()
        bot.send_message(self.message.chat.id, 'Fish was added successfully.')

    def edit_record(self, record_id, field, new_value, field_title):
        instance = Fish.objects.get(pk=record_id)
        setattr(instance, field, new_value)
        instance.save()
        bot.send_message(self.message.chat.id, f"{field_title} has been updated.",
                         reply_markup=main_menu_keyboard)

    def delete_record(self, record_id):
        try:
            fish_instance = Fish.objects.get(pk=record_id)
            fish_instance.delete()
            bot.send_message(self.message.chat.id, f"Selected record has been deleted!")

        except:
            bot.send_message(self.message.chat.id, 'You entered data incorrectly')
