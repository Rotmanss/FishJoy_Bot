import functools

import telebot

from bot.controllers.process_editing_record import EditRecord
from bot.father_bot import bot
from bot.forms import SpotsForm

from bot.views.spots_handler import SpotsHandler

from bot.controllers.process_adding_record import AddRecord


@bot.callback_query_handler(func=lambda call: call.data == 'spots')
def handle_get_spots(callback):
    bot.send_message(callback.message.chat.id, f"How much spots do you wan to see ?\nInput number greater than 0.")
    bot.register_next_step_handler(callback.message, lambda m: get_k_records(m))


def get_k_records(message):
    try:
        k = int(message.text)
        if k > 0:
            spots_handler = SpotsHandler(message)
            spots_handler.get_all_records(message.chat.id, k)
        else:
            raise ValueError
    except ValueError:
        sent = bot.send_message(message.chat.id, f"Your input is incorrect, please input number greater than 0.")
        bot.register_next_step_handler(sent, functools.partial(get_k_records))


@bot.callback_query_handler(func=lambda call: call.data == 'add_spot')
def handle_add_spots(callback):
    spots_handler = SpotsHandler(callback.message)
    field_name = ['title', 'location', 'max_depth', 'spot_category']
    field_description = [
        '<i>Title</i>',
        '<i>Location (in format - latitude, longitude. *Hint, you can take this data on google maps)</i>',
        '<i>Max depth in meters</i>',
        '<i>Spot category ids:\n1 - Lake, 2 - River, 3 - Sea, 4 - Ocean</i>'
    ]

    bot.send_message(callback.message.chat.id, f'To return to the main menu type x')
    add_spot = AddRecord(callback, field_name, field_description, spots_handler, SpotsForm)

    add_spot.ask_for_input(0)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_spot'))
def handle_edit_spots(callback):
    spots_handler = SpotsHandler(callback.message)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Title'),
                 telebot.types.KeyboardButton('Location'),
                 telebot.types.KeyboardButton('Max depth'),
                 telebot.types.KeyboardButton('Spot category'),
                 telebot.types.KeyboardButton('Photo'))
    field_name = {'Title': 'title', 'Location': 'location', 'Max depth': 'max_depth',
                  'Spot category': 'spot_category'}
    field_description = {
        'Title': '<i>Title</i>',
        'Location': '<i>Location (in format - latitude, longitude. *Hint, you can take this data on google maps)</i>',
        'Max depth': '<i>Max depth in meters</i>',
        'Spot category': '<i>Spot category ids:\n1 - Lake, 2 - River, 3 - Sea, 4 - Ocean</i>'
    }

    bot.send_message(callback.message.chat.id, f'To return to the main menu type x')
    edit_spot = EditRecord(callback, keyboard, field_name, field_description, spots_handler, SpotsForm)

    edit_spot.ask_for_field()


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_spot'))
def handle_delete_spots(callback):
    bot.send_message(callback.message.chat.id, "To delete this record type 1, to cancel type 0")
    spot_id = callback.data.split('_')[-1]

    bot.register_next_step_handler(callback.message, lambda m: process_delete_spot(m, spot_id))


def process_delete_spot(message, spot_id):
    if message.text == '1':
        spots_handler = SpotsHandler(message)
        spots_handler.delete_record(record_id=spot_id)
    else:
        bot.send_message(message.chat.id, f"You canceled deletion")
