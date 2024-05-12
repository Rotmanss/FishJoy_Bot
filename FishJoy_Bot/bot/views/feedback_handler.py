from django.contrib.auth.models import User

from bot.go_back import go_back
from bot.models import Feedback
from bot.father_bot import bot


def feedback(message):
    if go_back(message):
        return

    Feedback.objects.create(user_id=User.objects.get(username=str(message.from_user.id)).id, subject=message.text)
    bot.send_message(message.chat.id, 'Your feedback has been sent.')
