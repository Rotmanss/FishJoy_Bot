import logging

import telebot
from telebot.async_telebot import types

from django.conf import settings

from bot.middleware import CustomMiddleware
from bot.models import Spots, Baits, Fish

import re

# from FishJoy_Bot.database.spots_crud import add_spot

bot = telebot.TeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)

bot.setup_middleware(CustomMiddleware())


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

    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Spots':
        photo = 'AgACAgIAAxkBAAPmZgp3cwABhLE4BMdIQaTVrttbKafQAALZ4zEbOEZQSGkjdNm_ZtTWAQADAgADcwADNAQ'
        result = ''
        for spot in get_all_spots():
            for key, value in spot.items():
                if key == 'photo':
                    photo = f'{value}'
                    continue
                result += f'<b>{key}</b> : {value}\n'
            bot.send_photo(message.chat.id, photo, result)

            result = ''

    if message.text == 'Fish':
        result = 'All fish:\n'
        for key, value in get_all_fish().items():
            if key == 'photo':
                photo = f'{value}'
                continue
            result += f'<b>{key}</b> : {value}\n'

    if message.text == 'Baits':
        result = 'All baits:\n'
        for key, value in get_all_baits().items():
            if key == 'photo':
                photo = f'{value}'
                continue
            result += f'<b>{key}</b> : {value}\n'

    keyboard = types.InlineKeyboardMarkup(row_width=2)

    best_rating_button = types.InlineKeyboardButton('Best rating', callback_data='best_rating')
    newest_button = types.InlineKeyboardButton('Newest', callback_data='newest')

    keyboard.add(best_rating_button, newest_button)

    bot.send_message(message.chat.id, 'Filter by', reply_markup=keyboard)

    if message.text == 'Add spot':
        sent = bot.send_message(message.chat.id, 'Input spot details like this ..., separated with semicolon')
        bot.register_next_step_handler(sent, add_spot)


def get_all_spots():
    return list(Spots.objects.all().values())


@bot.callback_query_handler(func=lambda call: call.data == 'best_rating')
def get_best_rating(callback):
    Spots.objects.order_by('-rating')
    bot.send_message(callback.message.chat.id, 'BEST RATING')


@bot.callback_query_handler(func=lambda call: call.data == 'newest')
def get_best_rating(callback):
    bot.send_message(callback.message.chat.id, 'NEWEST')


def get_all_fish():
    return list(Fish.objects.all().values())[0]


def get_all_baits():
    return list(Baits.objects.all().values())[0]


def add_spot(message):
    print('CHEEEEEEEEKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')
    print('SUCCESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', message.caption)

    print('HERRRRRRRRREEEEEEEEEEEEEEEEE', message)
    if not message.photo:
        bot.send_message(message.chat.id, 'Provide a photo')
        return

    try:
        input_string = message.caption

        pattern = r'([^;]+)'
        result = re.findall(pattern, input_string)

        print('RESUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUULT', result)
        print('PHOOOOOOOOOOOTOOOOOOOOOOOOOOOOOO', message.photo)

        bot.send_photo(message.chat.id, message.photo[0].file_id)
        spot = Spots.objects.create(title=result[0].strip(),
                                    slug=result[1].strip(),
                                    rating=result[2].strip(),
                                    location=result[3].strip(),
                                    photo=message.photo[0].file_id,
                                    max_depth=result[4].strip(),
                                    likes=result[5].strip(),
                                    dislikes=result[6].strip(),
                                    spot_category_id=result[7].strip(),
                                    user_id=result[7].strip())
        spot.save()
    except:
        bot.send_message(message.chat.id, 'You entered data incorrectly')

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
