import functools

from bot.father_bot import bot
from bot.go_back import go_back


class AddRecord:
    def __init__(self, callback, field_name, field_description, handler, validation_form):
        self.callback = callback
        self.field_name = field_name
        self.field_description = field_description
        self.handler = handler
        self.validation_form = validation_form

        self.input_data = {}

    def ask_for_input(self, field_index):
        if field_index < len(self.field_description):
            field_descr = self.field_description[field_index]
            sent = bot.send_message(self.callback.message.chat.id, f'Please enter {field_descr}:')

            bot.register_next_step_handler(sent, lambda message, index=field_index: self.handle_input(message, index))
        else:
            self.ask_for_photo()

    def handle_input(self, message, index):
        if go_back(message):
            return

        field = self.field_name[index]
        form = self.validation_form({f'{field}': message.text})

        if form.is_valid():
            self.input_data[field] = message.text.strip()

            next_index = index + 1
            self.ask_for_input(next_index)
        else:
            sent = bot.send_message(self.callback.message.chat.id, 'You inputted data incorrectly. Try again.')
            bot.register_next_step_handler(sent, functools.partial(self.handle_input, index=index))

    def ask_for_photo(self):
        sent = bot.send_message(self.callback.message.chat.id, 'Please provide a photo:')
        bot.register_next_step_handler(sent, self.handle_photo)

    def handle_photo(self, message):
        if go_back(message):
            return

        if message.photo:
            self.input_data['photo'] = message.photo[0].file_id
            self.input_data['user_id'] = message.from_user.id
            self.handler.add_record(self.input_data)
        else:
            sent = bot.send_message(self.callback.message.chat.id, 'No photo attached. Please attach a photo.')
            bot.register_next_step_handler(sent, self.handle_photo)
