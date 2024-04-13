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
