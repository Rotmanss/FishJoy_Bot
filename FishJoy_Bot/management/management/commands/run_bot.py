import asyncio
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from bot.main_bot import bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Launch bot"

    def handle(self, *args, **options):
        try:
            bot.infinity_polling(logger_level=settings.LOG_LEVEL)
        except Exception as err:
            logger.error(f'Error: {err}')
