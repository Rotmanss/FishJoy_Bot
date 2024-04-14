from bot.forms import FishForm
from bot.handlers.base_nadler import Handler
from bot.models import Fish, FishCategory

from django.contrib.auth.models import User
import re
from telebot.async_telebot import types

from bot import main_menu_keyboard


class FishHandler(Handler):
    def __init__(self, bot, message):
        self.bot = bot
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

            self.bot.send_photo(self.message.chat.id, photo, caption=result, reply_markup=keyboard)

            result = ''

    @staticmethod
    def _get_from_db():
        return list(Fish.objects.all().values())

    def add_record(self, message):
        if not message.photo:
            self.bot.send_message(message.chat.id, 'Provide a photo')
            return

        try:
            input_string = message.caption

            pattern = r'([^;]+)'
            result = re.findall(pattern, input_string)

            form = FishForm({'name': result[0],
                              'average_weight': result[1],
                              'fish_category': result[2]})
            if form.is_valid():
                self.bot.send_photo(message.chat.id, message.photo[0].file_id)
                fish = Fish.objects.create(name=result[0].strip(),
                                            photo=message.photo[0].file_id,
                                            average_weight=result[1].strip(),
                                            user_id=User.objects.get(username=str(message.from_user.id)).id,
                                            fish_category_id=result[2].strip())
                fish.save()
            else:
                errors = form.errors.as_text()
                self.bot.send_message(message.chat.id, f"Validation errors: {errors}")
        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly')

    def edit_record(self, message, record_id, field_name, new_value):
        try:
            form = FishForm({f'{field_name}': new_value})

            if form.is_valid():
                fish_instance = Fish.objects.get(pk=record_id)
                setattr(fish_instance, field_name, new_value)
                fish_instance.save()
                self.bot.send_message(message.chat.id, f"{field_name.capitalize()} has been updated.", reply_markup=main_menu_keyboard)
            else:
                errors = form.errors.as_text()
                self.bot.send_message(message.chat.id, f"Validation error: {errors}", reply_markup=main_menu_keyboard)
        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly', reply_markup=main_menu_keyboard)

    def delete_record(self, message, record_id):
        try:
            fish_instance = Fish.objects.get(pk=record_id)
            fish_instance.delete()
            self.bot.send_message(message.chat.id, f"Selected record has been deleted!")

        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly')
