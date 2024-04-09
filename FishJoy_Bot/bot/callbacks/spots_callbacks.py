import telebot

from bot.father_bot import bot

from bot.handlers.spots_handler import SpotsHandler


@bot.callback_query_handler(func=lambda call: call.data == 'spots')
def handle_get_spots(callback):
    spots_handler = SpotsHandler(bot, callback.message)
    spots_handler.get_all_records(callback.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_spot')
def handle_add_spots(callback):
    spots_handler = SpotsHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, spots_handler.add_record)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_spot'))
def handle_edit_spots(callback):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('title'),
                 telebot.types.KeyboardButton('Field 2'),
                 telebot.types.KeyboardButton('Field 3'))
    bot.send_message(callback.message.chat.id, "Which field do you want to edit?", reply_markup=keyboard)

    spot_id = callback.data.split('_')[-1]
    bot.register_next_step_handler(callback.message, lambda m: process_selected_field_spots(m, spot_id))


def process_selected_field_spots(message, spot_id):
    field_name = message.text
    bot.send_message(message.chat.id, f"Please enter the new value for {field_name}", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda m: update_field_spots(m, field_name, spot_id))


def update_field_spots(message, field_name, spot_id):
    new_value = message.text

    spots_handler = SpotsHandler(bot, message)
    spots_handler.edit_record(message, record_id=spot_id, field_name=field_name, new_value=new_value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_spot'))
def handle_delete_spots(callback):
    spot_id = callback.data.split('_')[-1]

    spots_handler = SpotsHandler(bot, callback.message)
    spots_handler.delete_record(callback.message, record_id=spot_id)
    bot.send_message(callback.message.chat.id, f"Selected record has been deleted!")
