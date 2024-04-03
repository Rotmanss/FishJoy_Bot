from telebot import BaseMiddleware

from FishJoy_Bot.database.spots_crud import update_or_create_telegram_user


class CustomMiddleware(BaseMiddleware):
    def __init__(self):
        super(CustomMiddleware, self).__init__()
        self.update_sensitive = True
        self.update_types = ['message']

    def pre_process_message(self, message, data):
        my_data = None
        try:
            my_data = getattr(message, 'chat')
        except AttributeError:
            pass

        try:
            my_data = getattr(message, 'from_user')
        except AttributeError:
            pass

        if not my_data:
            return None
        if not message.text:
            return None

        update_or_create_telegram_user(my_data)

    def post_process_message(self, message, data, exception):
        pass # only message update here for post_process

    def pre_process_edited_message(self, message, data):
        # only edited_message update here
        pass

    def post_process_edited_message(self, message, data, exception):
        pass # only edited_message update here for post_process