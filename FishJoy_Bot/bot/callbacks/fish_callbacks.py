import telebot

from bot.father_bot import bot

from bot.handlers.fish_handler import FishHandler


@bot.callback_query_handler(func=lambda call: call.data == 'fish')
def handle_get_fish(callback):
    fish_handler = FishHandler(bot, callback.message)
    fish_handler.get_all_records(callback.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_fish')
def handle_add_fish(callback):
    fish_handler = FishHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, fish_handler.add_record)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_fish'))
def handle_edit_fish(callback):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('name'),
                 telebot.types.KeyboardButton('Field 2'),
                 telebot.types.KeyboardButton('Field 3'))
    bot.send_message(callback.message.chat.id, "Which field do you want to edit?", reply_markup=keyboard)

    fish_id = callback.data.split('_')[-1]
    bot.register_next_step_handler(callback.message, lambda m: process_selected_field_fish(m, fish_id))


def process_selected_field_fish(message, fish_id):
    field_name = message.text
    bot.send_message(message.chat.id, f"Please enter the new value for {field_name}", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda m: update_field_fish(m, field_name, fish_id))


def update_field_fish(message, field_name, fish_id):
    new_value = message.text

    fish_handler = FishHandler(bot, message)
    fish_handler.edit_record(record_id=fish_id, field_name=field_name, new_value=new_value)

    bot.send_message(message.chat.id, f"{field_name.capitalize()} has been updated to {new_value}.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_fish'))
def handle_delete_fish(callback):
    fish_id = callback.data.split('_')[-1]

    fish_handler = FishHandler(bot, callback.message)
    fish_handler.delete_record(record_id=fish_id)
    bot.send_message(callback.message.chat.id, f"Selected record has been deleted!")
