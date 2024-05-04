from bot.father_bot import bot
from bot.main_menu_keyboard import main_keyboard


def go_back(message):
    if message.text == 'x' or message.text == 'X':
        bot.send_message(message.chat.id, "Main menu", reply_markup=main_keyboard)
        return True
    return False
