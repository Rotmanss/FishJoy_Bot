from django.contrib.auth.models import User

from bot.models import Feedback
from bot.father_bot import bot


def feedback(message):
    Feedback.objects.create(user_id=User.objects.get(username=str(message.from_user.id)).id, subject=message.text)
    bot.send_message(message.chat.id, 'Your feedback has been sent.')
