import telebot

from bot.father_bot import bot

from bot.handlers.baits_handler import BaitsHandler


@bot.callback_query_handler(func=lambda call: call.data == 'baits')
def handle_get_baits(callback):
    baits_handler = BaitsHandler(bot, callback.message)
    baits_handler.get_all_records(callback.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_bait')
def handle_add_baits(callback):
    baits_handler = BaitsHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, baits_handler.add_record)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_bait'))
def handle_edit_baits(callback):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('name'),
                 telebot.types.KeyboardButton('Field 2'),
                 telebot.types.KeyboardButton('Field 3'))
    bot.send_message(callback.message.chat.id, "Which field do you want to edit?", reply_markup=keyboard)

    bait_id = callback.data.split('_')[-1]
    bot.register_next_step_handler(callback.message, lambda m: process_selected_field_baits(m, bait_id))


def process_selected_field_baits(message, bait_id):
    field_name = message.text
    bot.send_message(message.chat.id, f"Please enter the new value for {field_name}", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda m: update_field_spots(m, field_name, bait_id))


def update_field_spots(message, field_name, bait_id):
    new_value = message.text

    baits_handler = BaitsHandler(bot, message)
    baits_handler.edit_record(record_id=bait_id, field_name=field_name, new_value=new_value)

    bot.send_message(message.chat.id, f"{field_name.capitalize()} has been updated to {new_value}.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_bait'))
def handle_delete_fish(callback):
    bait_id = callback.data.split('_')[-1]

    baits_handler = BaitsHandler(bot, callback.message)
    baits_handler.delete_record(record_id=bait_id)
    bot.send_message(callback.message.chat.id, f"Selected record has been deleted!")
