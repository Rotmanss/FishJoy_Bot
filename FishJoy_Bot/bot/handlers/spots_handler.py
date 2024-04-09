from bot.handlers.base_nadler import Handler
from bot.main_menu_keyboard import main_keyboard
from bot.models import Spots

from telebot.async_telebot import types

from django.contrib.auth.models import User
from bot.forms import SpotsForm

import re


class SpotsHandler(Handler):
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def get_all_records(self, current_user_id):
        result = ''
        photo = 'AgACAgIAAxkBAAPmZgp3cwABhLE4BMdIQaTVrttbKafQAALZ4zEbOEZQSGkjdNm_ZtTWAQADAgADcwADNAQ'
        for spot in self._get_from_db():
            for key, value in spot.items():
                if key == 'photo':
                    photo = f'{value}'
                    continue

                if key == 'id':
                    id = value
                    continue

                if key == 'time_create' or key == 'time_update':
                    value = value.strftime('%B %d, %Y %I:%M %p')

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                if key == 'user_id' and str(value) == str(User.objects.get(username=current_user_id).id):
                    edit = types.InlineKeyboardButton("Edit spot", callback_data=f"edit_spot_{id}")
                    delete = types.InlineKeyboardButton("Delete spot", callback_data=f"delete_spot_{id}")
                    keyboard.add(edit, delete)
                    continue
                elif key == 'user_id':
                    continue

                result += f'<b>{key}</b> : {value}\n'

            self.bot.send_photo(self.message.chat.id, photo, caption=result, reply_markup=keyboard)

            result = ''

    @staticmethod
    def _get_from_db():
        return list(Spots.objects.all().values())

    def add_record(self, message):
        if not message.photo:
            self.bot.send_message(message.chat.id, 'You sent message without photo, press the button \'Add spots\' again')
            return

        try:
            input_string = message.caption

            pattern = r'([^;]+)'
            result = re.findall(pattern, input_string)

            form = SpotsForm({'title': result[0],
                              'location': result[1],
                              'max_depth': result[2],
                              'spot_category': result[3]})
            if form.is_valid():
                spot = Spots.objects.create(title=result[0].strip(),
                                            location=result[1].strip(),
                                            photo=message.photo[0].file_id,
                                            max_depth=result[2].strip(),
                                            spot_category_id=result[3].strip(),
                                            user_id=User.objects.get(username=str(message.from_user.id)).id)
                spot.save()
                self.bot.send_message(message.chat.id, 'Spot was added successfully.')
            else:
                errors = form.errors.as_text()
                self.bot.send_message(message.chat.id, f"Validation errors: {errors}")
        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly')

    def edit_record(self, message, record_id, field_name, new_value):
        try:
            form = SpotsForm({f'{field_name}': new_value})

            if form.is_valid():
                spot_instance = Spots.objects.get(pk=record_id)
                setattr(spot_instance, field_name, new_value)
                spot_instance.save()
                self.bot.send_message(message.chat.id, f"{field_name.capitalize()} has been updated to {new_value}.")
            else:
                errors = form.errors.as_text()
                self.bot.send_message(message.chat.id, f"Validation error: {errors}")
        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly')

    def delete_record(self, message, record_id):
        try:
            spot_instance = Spots.objects.get(pk=record_id)
            spot_instance.delete()
            self.bot.send_message(message.chat.id, f"Selected record has been deleted!")

        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly')
