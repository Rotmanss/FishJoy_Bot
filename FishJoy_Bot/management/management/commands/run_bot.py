import asyncio

from django.core.management.base import BaseCommand, CommandError

from bot.main_bot import bot


class Command(BaseCommand):
    help = "Launch bot"

    def handle(self, *args, **options):
        asyncio.run(bot.polling())
