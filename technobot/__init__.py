from technobot import api
from technobot import utils
from threading import Timer
from technobot import database
from functools import wraps


class TechnoBot:
    def __init__(self, token, ignore_old=False, timeout=3):
        self.token = token
        self._ignore_old = ignore_old
        self._timeout = timeout
        self._last_update_id = ignore_old
        self._updates = {}
        self._conversations = {}
        self._pre_handlers = {}
        self._thread = Timer(self._timeout, self._process_updates)

    def _receive_updates(self):
        self._updates = {}
        updates = api.get_updates(self.token, self._last_update_id)
        for update in updates:
            new_update = utils.Update(update)
            if self._ignore_old:
                self._last_update_id = new_update.update_id
                continue
            if self._last_update_id is not None and new_update.update_id > self._last_update_id:
                self._updates[new_update.update_id] = new_update
                self._last_update_id = new_update.update_id
            elif self._last_update_id is None:
                self._updates[new_update.update_id] = new_update
        self._ignore_old = False

    def _process_updates(self):
        self._receive_updates()
        self._thread.cancel()
        for update_id, update in self._updates.items():
            message = update.message
            if message is None: break
            if not(database.db_get_user(message.from_user.id)):
                database.db_register_user(message.from_user)
            self._process_conversation(message)

        self._thread = Timer(self._timeout, self._process_updates)
        self._thread.start()

    def _process_conversation(self, message):
        if message.chat.id in self._conversations:
            if self._conversations[message.chat.id].send(message):
                return True
            else:
                del (self._conversations[message.chat.id])
        elif message.text in self._pre_handlers:
            started_coroutine = self._pre_handlers[message.text](message)
            self._conversations[message.chat.id] = started_coroutine
        return False

    def conversation(self, handler=None):
        def _outer_decorator(func):
            def _decorator(*args, **kwargs):
                result = func(*args, **kwargs)
                return result
            self._pre_handlers[handler] = Conversation(func)
            return wraps(func)(_decorator)

        return _outer_decorator

    def send_message(self, chat_id, text):
        api.send_message(self.token, chat_id=chat_id, text=text)

    def polling(self):
        self._process_updates()


class Conversation:
    def __init__(self, coroutine):
        self._coroutine = coroutine
        self._initialized = False

    def send(self, message):
        try:
            self._coroutine.send(message)
            return True
        except StopIteration:
            return False

    def __call__(self, *args, **kwargs):
        self._coroutine = self._coroutine(*args, **kwargs)
        next(self._coroutine)
        return self








