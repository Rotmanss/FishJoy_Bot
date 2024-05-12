import telebot

from bot.controllers.process_adding_record import AddRecord
from bot.controllers.process_editing_record import EditRecord
from bot.forms import FishForm
from bot.father_bot import bot

from bot.views.fish_handler import FishHandler


@bot.callback_query_handler(func=lambda call: call.data == 'fish')
def handle_get_fish(callback):
    fish_handler = FishHandler(callback.message)
    fish_handler.get_all_records(callback.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_fish')
def handle_add_fish(callback):
    fish_handler = FishHandler(callback.message)
    field_name = ['name', 'average_weight', 'fish_category']
    field_description = [
        '<i>Name</i>',
        '<i>Average weight in kilograms</i>',
        '<i>Fish category ids:\n1 - Peaceful, 2 - Predatory</i>'
    ]

    bot.send_message(callback.message.chat.id, f'To return to the main menu type x')
    add_fish = AddRecord(callback, field_name, field_description, fish_handler, FishForm)

    add_fish.ask_for_input(0)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_fish'))
def handle_edit_fish(callback):
    fish_handler = FishHandler(callback.message)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Name'),
                 telebot.types.KeyboardButton('Average weight'),
                 telebot.types.KeyboardButton('Fish category'),
                 telebot.types.KeyboardButton('Photo'))

    field_name = {'Name': 'name', 'Average weight': 'average_weight', 'Fish category': 'fish_category'}
    field_description = {
        'Name': '<i>Name</i>',
        'Average weight': '<i>Average weight in kilograms</i>',
        'Fish category': '<i>Fish category ids:\n1 - Peaceful, 2 - Predatory</i>'
    }

    bot.send_message(callback.message.chat.id, f'To return to the main menu type x')
    edit_fish = EditRecord(callback, keyboard, field_name, field_description, fish_handler, FishForm)

    edit_fish.ask_for_field()


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_fish'))
def handle_delete_fish(callback):
    bot.send_message(callback.message.chat.id, "To delete this record type 1, to cancel type 0")
    fish_id = callback.data.split('_')[-1]

    bot.register_next_step_handler(callback.message, lambda m: process_delete_fish(m, fish_id))


def process_delete_fish(message, fish_id):
    if message.text == '1':
        fish_handler = FishHandler(message)
        fish_handler.delete_record(record_id=fish_id)
    else:
        bot.send_message(message.chat.id, f"You canceled deletion")
