import logging

from asgiref.sync import sync_to_async
from telebot.types import Chat, User

from bot.models import BotUser
# from bot.main_bot import bot

logger = logging.getLogger(__name__)





def update_or_create_telegram_user(data: Chat | User):
    try:
        data = getattr(data, 'chat')
    except:
        pass

    first_name = data.first_name
    if not data.first_name:
        first_name = ''

    last_name = data.last_name
    if not data.last_name:
        last_name = ''

    username = data.username
    if not data.username:
        username = ''

    defaults_dict = {
        'first_name': first_name,
        'last_name' : last_name,
        'username' : username
    }

    telegram_user, create_status = BotUser.objects.update_or_create(telegram_id=data.id, defaults=defaults_dict)
    if create_status is False:
        logger.info(f'User was updated {first_name} {last_name} {username}')
    else:
        logger.info(f'User was created {first_name} {last_name} {username}')
    return create_status
