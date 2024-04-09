from telebot.async_telebot import types

from bot.father_bot import bot
from bot.validators import is_telegram_user_registered


main_keyboard = types.InlineKeyboardMarkup(row_width=3)

main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_button = types.KeyboardButton("Main menu")
main_menu_keyboard.add(main_menu_button)

ADD_ONCE = False


def init_keyboard(message):
    spots_button = types.InlineKeyboardButton('Spots', callback_data='spots')
    fish_button = types.InlineKeyboardButton('Fish', callback_data='fish')
    baits_button = types.InlineKeyboardButton('Baits', callback_data='baits')

    add_spot_button = types.InlineKeyboardButton('Add spots', callback_data='add_spot')
    add_fish_button = types.InlineKeyboardButton('Add fish', callback_data='add_fish')
    add_bait_button = types.InlineKeyboardButton('Add baits', callback_data='add_bait')

    if not main_keyboard.keyboard:
        main_keyboard.add(spots_button, fish_button, baits_button)

    if is_telegram_user_registered(message.from_user.id):
        global ADD_ONCE
        if not ADD_ONCE:
            main_keyboard.add(add_spot_button, add_fish_button, add_bait_button)
            ADD_ONCE = True
    else:
        bot.send_message(message.chat.id, (
            "If you want to add information, you need to register your account first. For now you can only read.\n\n"
            "To register your account type /register. "))
