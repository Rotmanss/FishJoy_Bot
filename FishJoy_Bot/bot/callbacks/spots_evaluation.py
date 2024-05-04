from django.contrib.auth.models import User

from bot.father_bot import bot
from bot.forms import EvaluationForm
from bot.go_back import go_back
from bot.models import Spots, Evaluation


@bot.callback_query_handler(func=lambda call: call.data.startswith('evaluate'))
def evaluate(callback):
    spot_id = callback.data.split('_')[-1]
    spot = Spots.objects.get(pk=spot_id)

    if not Evaluation.objects.filter(user_id=User.objects.get(username=str(callback.from_user.id)).id, record_id=spot_id).exists():
        bot.send_message(callback.message.chat.id, "Please rate this record from 1 to 5, where 5 is very good.\n"
                                                   "To return to the main menu type x")
        bot.register_next_step_handler(callback.message, lambda m: process_rating(m, spot_id))
    else:
        bot.send_message(callback.message.chat.id, f"You can evaluate only once!\nThe average rating is {spot.average_rating:.1f}")


def process_rating(message, spot_id):
    if go_back(message):
        return

    rating = float(message.text)
    record = Spots.objects.get(pk=spot_id)

    form = EvaluationForm({'rating': rating})
    if form.is_valid():

        Evaluation.objects.create(record=record, user_id=User.objects.get(username=str(message.from_user.id)).id, rating=rating)

        Evaluation.update_average_rating_for_record_id(spot_id)
        record = Spots.objects.get(pk=spot_id)

        bot.send_message(message.chat.id, f"Thank you for your rating! The average rating for this record is now {record.average_rating:.1f}")
    else:
        errors = form.errors.as_text()
        bot.send_message(message.chat.id, f"Validation errors: {errors}")
