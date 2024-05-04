import telebot

from bot.father_bot import bot

from bot.handlers.spots_handler import SpotsHandler
from bot.models import Spots

from bot.main_menu_keyboard import main_menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'spots')
def handle_get_spots(callback):
    spots_handler = SpotsHandler(bot, callback.message)
    spots_handler.get_all_records(callback.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_spot')
def handle_add_spots(callback):
    spots_handler = SpotsHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id,
                            ('Input spot details in one line, separated with semicolon:\n'
                             '<i>Title</i>;\n'
                             '<i>Location (in format - latitude, longitude. '
                             '*Hint, you can take this data on google maps)</i>;\n'
                             '<i>Max depth in meters</i>;\n'
                             '<i>Spot category ids:\n'
                             '1 - Lake, 2 - River, 3 - Sea, 4 - Ocean</i>\n'
                             'Attach photo and make sure details are separated with semicolon.\n'
                             'To return to the main menu type x or X'))

    bot.register_next_step_handler(sent, spots_handler.add_record)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_spot'))
def handle_edit_spots(callback):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Title'),
                 telebot.types.KeyboardButton('Location'),
                 telebot.types.KeyboardButton('Max depth'),
                 telebot.types.KeyboardButton('Spot category id'),
                 telebot.types.KeyboardButton('Photo'))
    bot.send_message(callback.message.chat.id,
                     "Which field do you want to edit?\n(*Hint - You have a menu to "
                     "pick a field to edit on the right side from your keyboard)", reply_markup=keyboard)

    spot_id = callback.data.split('_')[-1]
    bot.register_next_step_handler(callback.message, lambda m: process_selected_field_spots(m, spot_id))


def process_selected_field_spots(message, spot_id):
    field_name = message.text.lower()
    if field_name in [field.name for field in Spots._meta.get_fields()]:
        bot.send_message(message.chat.id, f"Please enter the new value for {field_name}",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, lambda m: update_field_spots(m, field_name, spot_id))
    else:
        bot.send_message(message.chat.id, "The field name you provided does not exist", reply_markup=main_menu_keyboard)


def update_field_spots(message, field_name, spot_id):
    if field_name == 'photo':
        new_value = message.photo[0].file_id
    else:
        new_value = message.text

    spots_handler = SpotsHandler(bot, message)
    spots_handler.edit_record(message, record_id=spot_id, field_name=field_name, new_value=new_value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_spot'))
def handle_delete_spots(callback):
    bot.send_message(callback.message.chat.id, "To delete this record type 1, to cancel type 0")
    spot_id = callback.data.split('_')[-1]

    bot.register_next_step_handler(callback.message, lambda m: process_delete_spot(m, spot_id))


def process_delete_spot(message, spot_id):
    if message.text == '1':
        spots_handler = SpotsHandler(bot, message)
        spots_handler.delete_record(message, record_id=spot_id)
    else:
        bot.send_message(message.chat.id, f"You canceled deletion")
