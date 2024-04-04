import logging

import telebot
from telebot.async_telebot import types

from django.conf import settings
from django.contrib.auth.models import User

from bot.handlers.spots_handler import SpotsHandler
from bot.handlers.fish_handler import FishHandler
from bot.handlers.baits_handler import BaitsHandler


bot = telebot.TeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['register'])
def register_user(message):
    user_telegram_id = message.from_user.id
    User.objects.get_or_create(username=str(user_telegram_id))


def is_telegram_user_registered(telegram_id):
    try:
        User.objects.get(username=str(telegram_id))
        return True
    except User.DoesNotExist:
        return False


@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    spots_button = types.InlineKeyboardButton('Spots', callback_data='spots')
    fish_button = types.InlineKeyboardButton('Fish', callback_data='fish')
    baits_button = types.InlineKeyboardButton('Baits', callback_data='baits')

    add_spot_button = types.InlineKeyboardButton('Add spots', callback_data='add_spot')
    add_fish_button = types.InlineKeyboardButton('Add fish', callback_data='add_fish')
    add_bait_button = types.InlineKeyboardButton('Add baits', callback_data='add_bait')

    keyboard.add(spots_button, fish_button, baits_button)

    if is_telegram_user_registered(message.from_user.id):
        keyboard.add(add_spot_button, add_fish_button, add_bait_button)
    else:
        bot.send_message(message.chat.id, ("If you want to add information, you need to register your account first.\n"
                                           "To register your account type /register"))

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}, here are your options:', reply_markup=keyboard)


# SPOTS
@bot.callback_query_handler(func=lambda call: call.data == 'spots')
def handle_get_spots(callback):
    spots_handler = SpotsHandler(bot, callback.message)
    spots_handler.get_all_records()


@bot.callback_query_handler(func=lambda call: call.data == 'add_spot')
def handle_add_spots(callback):
    spots_handler = SpotsHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, spots_handler.add_record)


# FISH
@bot.callback_query_handler(func=lambda call: call.data == 'fish')
def handle_get_fish(callback):
    fish_handler = FishHandler(bot, callback.message)
    fish_handler.get_all_records()


@bot.callback_query_handler(func=lambda call: call.data == 'add_fish')
def handle_add_fish(callback):
    fish_handler = FishHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, fish_handler.add_record)


# BAITS
@bot.callback_query_handler(func=lambda call: call.data == 'baits')
def handle_get_baits(callback):
    baits_handler = BaitsHandler(bot, callback.message)
    baits_handler.get_all_records()


@bot.callback_query_handler(func=lambda call: call.data == 'add_bait')
def handle_add_baits(callback):
    baits_handler = BaitsHandler(bot, callback.message)
    sent = bot.send_message(callback.message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, baits_handler.add_record)


# @bot.message_handler(content_types=['text'])
# def main_menu(message):
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#
#     best_rating_button = types.InlineKeyboardButton('Best rating', callback_data='best_rating')
#     newest_button = types.InlineKeyboardButton('Newest', callback_data='newest')
#
#     keyboard.add(best_rating_button, newest_button)
#
#     bot.send_message(message.chat.id, 'Filter by', reply_markup=keyboard)


# @bot.callback_query_handler(func=lambda call: call.data == 'best_rating')
# def get_best_rating(callback):
#     Spots.objects.order_by('-rating')
#     bot.send_message(callback.message.chat.id, 'BEST RATING')
#
#
# @bot.callback_query_handler(func=lambda call: call.data == 'newest')
# def get_best_rating(callback):
#     bot.send_message(callback.message.chat.id, 'NEWEST')



    # title, slug, rating, location, max depth, likes, dislikes, spot category id, user_id
    # test2; test2; 5; Gdansk; 50; 1; 0; 1; 1


# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     btn = types.InlineKeyboardButton(text='Add fish', callback_data='add_spot')
#     keyboard.add(btn)
#     bot.send_message(message.chat.id, reply_markup=keyboard, text='success')
#
#
# @bot.callback_query_handler(func=lambda callback: callback.data)
# def check_callback_data(callback):
#     sent = bot.send_message(callback.message.chat.id, 'Enter details')
#     bot.register_next_step_handler(sent, review)
#
#
# def review(message):
#     bot.send_message(message.chat.id, text=f'Your data {message.text}')
#
#
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)
