import telebot

from bot.main_menu_keyboard import main_menu_keyboard
from bot.father_bot import bot

from bot.handlers.baits_handler import BaitsHandler
from bot.models import Baits


@bot.callback_query_handler(func=lambda call: call.data == 'baits')
def handle_get_baits(callback):
    baits_handler = BaitsHandler(bot, callback.message)
    baits_handler.get_all_records(callback.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_bait')
def handle_add_baits(callback):
    baits_handler = BaitsHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id,
                            ('Input bait details in one line, separated with semicolon:\n'
                             '<i>Name</i>;\n'
                             '<i>Price in dollars</i>\n'
                             'Attach photo and make sure details are separated with semicolon.\n'
                             'To return to the main menu type x'))

    bot.register_next_step_handler(sent, baits_handler.add_record)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_bait'))
def handle_edit_baits(callback):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Name'),
                 telebot.types.KeyboardButton('Price'),
                 telebot.types.KeyboardButton('Photo'))
    bot.send_message(callback.message.chat.id, "Which field do you want to edit?", reply_markup=keyboard)

    bait_id = callback.data.split('_')[-1]
    bot.register_next_step_handler(callback.message, lambda m: process_selected_field_baits(m, bait_id))


def process_selected_field_baits(message, bait_id):
    field_name = message.text.lower
    if message.text in [field.name for field in Baits._meta.get_fields()]:
        bot.send_message(message.chat.id, f"Please enter the new value for {field_name}", reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, lambda m: update_field_spots(m, field_name, bait_id))
    else:
        bot.send_message(message.chat.id, "The field name you provided does not exist", reply_markup=main_menu_keyboard)


def update_field_spots(message, field_name, bait_id):
    field_name = field_name.lower()
    if field_name == 'photo':
        new_value = message.photo[0].file_id
    else:
        new_value = message.text

    baits_handler = BaitsHandler(bot, message)
    baits_handler.edit_record(message, record_id=bait_id, field_name=field_name, new_value=new_value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_bait'))
def handle_delete_bait(callback):
    bot.send_message(callback.message.chat.id, "To delete this record type 1, to cancel type 0")
    bait_id = callback.data.split('_')[-1]

    bot.register_next_step_handler(callback.message, lambda m: process_delete_bait(m, bait_id))


def process_delete_bait(message, bait_id):
    if message.text == '1':
        baits_handler = BaitsHandler(bot, message)
        baits_handler.delete_record(message, record_id=bait_id)
    else:
        bot.send_message(message.chat.id, f"You canceled deletion")
