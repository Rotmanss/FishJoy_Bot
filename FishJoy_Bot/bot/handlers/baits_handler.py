from bot.handlers.base_nadler import Handler
from bot.models import Baits
from telebot.async_telebot import types


from django.contrib.auth.models import User
import re


class BaitsHandler(Handler):
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def get_all_records(self, current_user_id):
        result = ''
        photo = 'AgACAgIAAxkBAAPmZgp3cwABhLE4BMdIQaTVrttbKafQAALZ4zEbOEZQSGkjdNm_ZtTWAQADAgADcwADNAQ'
        for bait in self._get_from_db():
            for key, value in bait.items():
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
                    edit = types.InlineKeyboardButton("Edit bait", callback_data=f"edit_bait_{id}")
                    delete = types.InlineKeyboardButton("Delete bait", callback_data=f"delete_bait_{id}")
                    keyboard.add(edit, delete)
                    continue
                elif key == 'user_id':
                    continue

                result += f'<b>{key}</b> : {value}\n'

            self.bot.send_photo(self.message.chat.id, photo, caption=result, reply_markup=keyboard)

            result = ''

    @staticmethod
    def _get_from_db():
        return list(Baits.objects.all().values())

    def add_record(self, message):
        if not message.photo:
            self.bot.send_message(message.chat.id, 'Provide a photo')
            return

        try:
            input_string = message.caption

            pattern = r'([^;]+)'
            result = re.findall(pattern, input_string)

            self.bot.send_photo(message.chat.id, message.photo[0].file_id)
            bait = Baits.objects.create(name=result[0].strip(),
                                        photo=message.photo[0].file_id,
                                        price=result[1].strip(),
                                        user_id=User.objects.get(username=str(message.from_user.id)).id)
            bait.save()
        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly')

    def edit_record(self, record_id, field_name, new_value):
        bait_instance = Baits.objects.get(pk=record_id)
        setattr(bait_instance, field_name, new_value)
        bait_instance.save()

    def delete_record(self, record_id):
        bait_instance = Baits.objects.get(pk=record_id)
        bait_instance.delete()
