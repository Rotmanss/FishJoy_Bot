from bot.handlers.base_nadler import Handler
from bot.models import Spots

from django.contrib.auth.models import User
import re


class SpotsHandler(Handler):
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def get_all_records(self):
        result = ''
        photo = 'AgACAgIAAxkBAAPmZgp3cwABhLE4BMdIQaTVrttbKafQAALZ4zEbOEZQSGkjdNm_ZtTWAQADAgADcwADNAQ'
        for spot in self._get_from_db():
            for key, value in spot.items():
                if key == 'photo':
                    photo = f'{value}'
                    continue
                result += f'<b>{key}</b> : {value}\n'
            self.bot.send_photo(self.message.chat.id, photo, result)

            result = ''

    @staticmethod
    def _get_from_db():
        return list(Spots.objects.all().values())

    def add_record(self, message):
        if not message.photo:
            self.bot.send_message(message.chat.id, 'Provide a photo')
            return

        try:
            input_string = message.caption

            pattern = r'([^;]+)'
            result = re.findall(pattern, input_string)

            print('RESUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUULT', result)

            self.bot.send_photo(message.chat.id, message.photo[0].file_id)
            spot = Spots.objects.create(title=result[0].strip(),
                                        location=result[1].strip(),
                                        photo=message.photo[0].file_id,
                                        max_depth=result[2].strip(),
                                        spot_category_id=result[3].strip(),
                                        user_id=User.objects.get(username=str(message.from_user.id)).id)
            spot.save()
        except:
            self.bot.send_message(message.chat.id, 'You entered data incorrectly')
