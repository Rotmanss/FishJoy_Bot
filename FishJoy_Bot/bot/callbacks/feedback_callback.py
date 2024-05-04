from bot.father_bot import bot
from bot.handlers.feedback_handler import feedback


@bot.callback_query_handler(func=lambda call: call.data == 'feedback')
def handle_feedback(callback):
    sent = bot.send_message(callback.message.chat.id, 'Give a feedback.\n'
                                                      'To return to the main menu type x')

    bot.register_next_step_handler(sent, feedback)
