import logging

import telebot
from telebot.async_telebot import types

from bot.father_bot import bot
from bot.main_menu_keyboard import main_keyboard, main_menu_keyboard, init_keyboard

from django.conf import settings
from django.contrib.auth.models import User


from bot.callbacks.spots_callbacks import handle_get_spots, handle_add_spots, handle_edit_spots, handle_delete_spots
from bot.callbacks.fish_callbacks import handle_get_fish, handle_add_fish, handle_edit_fish, handle_delete_fish
from bot.callbacks.baits_callbacks import handle_get_baits, handle_add_baits
from bot.callbacks.feedback_callback import handle_feedback
from bot.callbacks.spots_evaluation import evaluate


from weather.weather_callback import handle_weather
from map.map_callback import handle_map


telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

SEND_ONCE = False


@bot.message_handler(commands=['register'])
def register_user(message):
    user_telegram_id = message.from_user.id
    User.objects.get_or_create(username=str(user_telegram_id))


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'Main menu')
def start_handler(message):
    init_keyboard(message)

    bot.send_message(message.chat.id, f'Main Menu', reply_markup=main_keyboard)
    global SEND_ONCE
    if not SEND_ONCE:
        bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}',  reply_markup=main_menu_keyboard)
        SEND_ONCE = True


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Press a button in main menu, or press /start.')
