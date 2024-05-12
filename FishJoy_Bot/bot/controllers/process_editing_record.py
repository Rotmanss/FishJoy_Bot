import functools

from bot.father_bot import bot
from bot.go_back import go_back
from bot.main_menu_keyboard import main_menu_keyboard
from bot.models import SpotCategory, FishCategory


class EditRecord:
    def __init__(self, callback, keyboard, field_name, field_description, handler, validation_form):
        self.message = callback.message
        self.keyboard = keyboard
        self.field_name = field_name
        self.field_description = field_description
        self.handler = handler
        self.validation_form = validation_form

        self.record_id = callback.data.split('_')[-1]

    def ask_for_field(self):
        sent = bot.send_message(self.message.chat.id,
                                "Which field do you want to edit?\n(*Hint - You have a menu to "
                                "pick a field to edit on the right side from your keyboard)", reply_markup=self.keyboard)

        bot.register_next_step_handler(sent, lambda message: self.process_selected_field(message))

    def process_selected_field(self, message):
        field_title = message.text
        if field_title in list(self.field_name.keys()):
            sent = bot.send_message(message.chat.id, f"Please enter the new value for {self.field_description[field_title]}",
                                    reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(sent, lambda m: self.handle_input(m, field_title))
        elif field_title == 'Photo':
            self.ask_for_photo()
        else:
            bot.send_message(message.chat.id, "The field name you provided does not exist. Try again.")
            self.ask_for_field()

    def handle_input(self, message, field_title):
        if go_back(message):
            return

        field = self.field_name[field_title]
        form = self.validation_form({f'{field}': message.text})

        if form.is_valid():
            new_value = message.text
            if field == 'spot_category':
                new_value = SpotCategory.objects.get(pk=new_value)
            elif field == 'fish_category':
                new_value = FishCategory.objects.get(pk=new_value)

            self.handler.edit_record(self.record_id, field, new_value, field_title)
        else:
            sent = bot.send_message(self.message.chat.id, 'You inputted data incorrectly. Try again.')
            bot.register_next_step_handler(sent, functools.partial(self.handle_input, field_title=field_title))

    def ask_for_photo(self):
        sent = bot.send_message(self.message.chat.id, 'Please provide a photo:')
        bot.register_next_step_handler(sent, self.handle_photo)

    def handle_photo(self, message):
        if go_back(message):
            return

        if message.photo:
            self.update('photo', message.photo[0].file_id, 'Photo')
        else:
            sent = bot.send_message(self.message.chat.id, 'No photo attached. Please attach a photo.')
            bot.register_next_step_handler(sent, self.handle_photo)
