from bot.father_bot import bot
from bot.views.base_handler import Handler
from bot.models import Baits
from telebot.async_telebot import types

from bot.main_menu_keyboard import main_menu_keyboard

from django.contrib.auth.models import User


class BaitsHandler(Handler):
    def __init__(self, message):
        self.message = message

    def get_all_records(self, current_user_id, k):
        result = ''
        photo = 'AgACAgIAAxkBAAPmZgp3cwABhLE4BMdIQaTVrttbKafQAALZ4zEbOEZQSGkjdNm_ZtTWAQADAgADcwADNAQ'
        for bait in self._get_from_db(k):
            for key, value in bait.items():
                if key == 'photo':
                    photo = f'{value}'
                    continue

                if key == 'id':
                    id = value
                    continue

                if key == 'time_create' or key == 'time_update':
                    value = value.strftime('%B %d, %Y %I:%M %p')

                elif key == 'price':
                    value = f'{value}$'

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                if key == 'user_id' and str(value) == str(User.objects.get(username=current_user_id).id):
                    edit = types.InlineKeyboardButton("Edit bait", callback_data=f"edit_bait_{id}")
                    delete = types.InlineKeyboardButton("Delete bait", callback_data=f"delete_bait_{id}")
                    keyboard.add(edit, delete)
                    continue
                elif key == 'user_id':
                    continue

                result += f'<b>{' '.join(word for word in key.capitalize().split('_'))}</b> : {value}\n'

            bot.send_photo(self.message.chat.id, photo, caption=result, reply_markup=keyboard)

            result = ''

    @staticmethod
    def _get_from_db(k):
        return list(Baits.objects.all()[:k].values())

    def add_record(self, data):
        bait = Baits.objects.create(name=data['name'],
                                    photo=data['photo'],
                                    price=data['price'],
                                    user_id=User.objects.get(username=str(data['user_id'])).id)
        bait.save()
        bot.send_message(self.message.chat.id, 'Bait was added successfully.')

    def edit_record(self, record_id, field, new_value, field_title):
        instance = Baits.objects.get(pk=record_id)
        setattr(instance, field, new_value)
        instance.save()
        bot.send_message(self.message.chat.id, f"{field_title} has been updated.",
                         reply_markup=main_menu_keyboard)

    def delete_record(self, record_id):
        try:
            bait_instance = Baits.objects.get(pk=record_id)
            bait_instance.delete()
            bot.send_message(self.message.chat.id, f"Selected record has been deleted!")

        except:
            bot.send_message(self.message.chat.id, 'You entered data incorrectly')