import functools

import telebot

from bot.controllers.process_adding_record import AddRecord
from bot.controllers.process_editing_record import EditRecord
from bot.forms import BaitsForm
from bot.father_bot import bot

from bot.views.baits_handler import BaitsHandler


@bot.callback_query_handler(func=lambda call: call.data == 'baits')
def handle_get_baits(callback):
    bot.send_message(callback.message.chat.id, f"How much baits do you wan to see ?\nInput number greater than 0.")
    bot.register_next_step_handler(callback.message, lambda m: get_k_records(m))


def get_k_records(message):
    try:
        k = int(message.text)
        if k > 0:
            baits_handler = BaitsHandler(message)
            baits_handler.get_all_records(message.chat.id, k)
        else:
            raise ValueError
    except ValueError:
        sent = bot.send_message(message.chat.id, f"Your input is incorrect, please input number greater than 0.")
        bot.register_next_step_handler(sent, functools.partial(get_k_records))


@bot.callback_query_handler(func=lambda call: call.data == 'add_bait')
def handle_add_baits(callback):
    baits_handler = BaitsHandler(callback.message)
    field_name = ['name', 'price']
    field_description = [
        '<i>Name</i>',
        '<i>Price in dollars</i>'
    ]

    bot.send_message(callback.message.chat.id, f'To return to the main menu type x')
    add_bait = AddRecord(callback, field_name, field_description, baits_handler, BaitsForm)

    add_bait.ask_for_input(0)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_bait'))
def handle_edit_baits(callback):
    baits_handler = BaitsHandler(callback.message)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Name'),
                 telebot.types.KeyboardButton('Price'),
                 telebot.types.KeyboardButton('Photo'))
    field_name = {'Name': 'name', 'Price': 'price'}
    field_description = {
        'Name': '<i>Name</i>',
        'Price': '<i>Price in dollars</i>'
    }

    bot.send_message(callback.message.chat.id, f'To return to the main menu type x')
    edit_bait = EditRecord(callback, keyboard, field_name, field_description, baits_handler, BaitsForm)

    edit_bait.ask_for_field()


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_bait'))
def handle_delete_bait(callback):
    bot.send_message(callback.message.chat.id, "To delete this record type 1, to cancel type 0")
    bait_id = callback.data.split('_')[-1]

    bot.register_next_step_handler(callback.message, lambda m: process_delete_bait(m, bait_id))


def process_delete_bait(message, bait_id):
    if message.text == '1':
        baits_handler = BaitsHandler(message)
        baits_handler.delete_record(record_id=bait_id)
    else:
        bot.send_message(message.chat.id, f"You canceled deletion")
