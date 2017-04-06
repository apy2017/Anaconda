from technobot import api
from technobot import utils
from threading import Timer
from technobot import database

class TechnoBot:
        def __init__(self, token, timeout=3):
        self.token = token
        self._timeout = timeout
        self._last_update_id = None
        self._updates = {}
        self._thread = Timer(self._timeout, self._process_updates)

    def _receive_updates(self):
        self._updates = {}
        updates = api.get_updates(self.token, self._last_update_id)
        for update in updates:
            new_update = utils.Update(update)
            if self._last_update_id is not None and new_update.update_id > self._last_update_id:
                self._last_update_id = new_update.update_id
                self._updates[new_update.update_id] = new_update
            elif self._last_update_id is None:
                self._last_update_id = new_update.update_id
                self._updates[new_update.update_id] = new_update

    def _process_updates(self):
        self._receive_updates()
        self._thread.cancel()
        for update_id, update in self._updates.items():
            if update.message is not None:
                message = update.message
                user = update.message.from_user
                database.db_register_user(user.id, user.first_name, user.last_name)
                self.send_message(message.chat.id, message.text)
        self._thread = Timer(self._timeout, self._process_updates)
        self._thread.start()

    def send_message(self, chat_id, text):
        api.send_message(self.token, chat_id=chat_id, text=text)

    def polling(self):
        self._process_updates()

