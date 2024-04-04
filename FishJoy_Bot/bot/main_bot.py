import logging

import telebot
from telebot.async_telebot import types

from django.conf import settings

from bot.handlers.spots_handler import SpotsHandler
from bot.handlers.fish_handler import FishHandler
from bot.handlers.baits_handler import BaitsHandler

bot = telebot.TeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    spots_button = types.KeyboardButton('Spots')
    fish_button = types.KeyboardButton('Fish')
    baits_button = types.KeyboardButton('Baits')

    add_spot_button = types.KeyboardButton('Add spot')
    add_fish_button = types.KeyboardButton('Add fish')
    add_bait_button = types.KeyboardButton('Add bait')

    keyboard.add(spots_button, fish_button, baits_button)
    keyboard.add(add_spot_button, add_fish_button, add_bait_button)

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}, here are your options:', reply_markup=keyboard)


# SPOTS
@bot.message_handler(func=lambda message: message.text == 'Spots')
def handle_get_spots(message):
    spots_handler = SpotsHandler(bot, message)
    spots_handler.get_all_records()


@bot.message_handler(func=lambda message: message.text == 'Add spot')
def handle_(message):
    spots_handler = SpotsHandler(bot, message)
    sent = bot.send_message(message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, spots_handler.add_record)


# FISH
@bot.message_handler(func=lambda message: message.text == 'Fish')
def handle_get_spots(message):
    fish_handler = FishHandler(bot, message)
    fish_handler.get_all_records()


@bot.message_handler(func=lambda message: message.text == 'Add fish')
def handle_(message):
    fish_handler = FishHandler(bot, message)
    sent = bot.send_message(message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, fish_handler.add_record)


# BAITS
@bot.message_handler(func=lambda message: message.text == 'Baits')
def handle_get_spots(message):
    baits_handler = BaitsHandler(bot, message)
    baits_handler.get_all_records()


@bot.message_handler(func=lambda message: message.text == 'Add bait')
def handle_(message):
    baits_handler = BaitsHandler(bot, message)
    sent = bot.send_message(message.chat.id, 'Input spot details like this ..., separated with semicolon')

    bot.register_next_step_handler(sent, baits_handler.add_record)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    best_rating_button = types.InlineKeyboardButton('Best rating', callback_data='best_rating')
    newest_button = types.InlineKeyboardButton('Newest', callback_data='newest')

    keyboard.add(best_rating_button, newest_button)

    bot.send_message(message.chat.id, 'Filter by', reply_markup=keyboard)


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
