import telebot
from django.conf import settings


bot = telebot.TeleBot(settings.TOKEN_BOT, parse_mode='HTML')
