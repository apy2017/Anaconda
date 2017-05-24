from technobot import api
from technobot import utils
from threading import Timer
from functools import wraps
import re
import copy


class TechnoBot:
    def __init__(self, token, exit_button=None, ignore_old=False, timeout=3):
        self.token = token
        self._exit_reply_button = exit_button
        self._ignore_old = ignore_old
        self._timeout = timeout
        self._last_update_id = ignore_old
        self._updates = {}
        self._conversations = {}
        # Pre Handlers for conversation coroutines
        self._pre_handlers = []
        self._handlers = []
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

    def receive_updates(self, updates):
        self._updates = {}
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

    def process_webhook_update(self, update):
        new_update = utils.Update(update)
        message = new_update.message
        if message is None: return
        self._process_conversation(message)
        self._process_handlers(message)

    def _process_updates(self):
        self._receive_updates()
        self._thread.cancel()
        for update_id, update in self._updates.items():
            message = update.message
            if message is None: break
            self._process_conversation(message)
            self._process_handlers(message)

        self._thread = Timer(self._timeout, self._process_updates)
        self._thread.start()

    def _process_conversation(self, message):
        if message.text == self._exit_reply_button.text:
            self._default_exit_handler(message)
        if message.chat.id in self._conversations:
            if self._conversations[message.chat.id].send(message):
                return None
            else:
                del (self._conversations[message.chat.id])
        elif len(self._pre_handlers)>0:
            handler_func = self._match_pre_handler(message)
            if handler_func is not None:
                started_coroutine = handler_func(message)
                self._conversations[message.chat.id] = started_coroutine

        return None

    def _process_handlers(self, message):
        if message.chat.id not in self._conversations:
            handler_func = self._match_handler(message)
            if handler_func is not None:
                handler_func(message)

    def _match_handler(self, message):
        for handler, handler_func in self._handlers:
            if re.match(handler, message.text):
                return handler_func
        return None

    def _match_pre_handler(self, message):
        for handler_obj in self._pre_handlers:
            handler, handler_func = handler_obj
            if re.match(handler, message.text):
                return copy.copy(handler_func)
        return None

    def _default_exit_handler(self, message):
        if message.chat.id in self._conversations:
            del self._conversations[message.chat.id]

    def conversation(self, handler=None):
        def _outer_decorator(func):
            def _decorator(*args, **kwargs):
                result = func(*args, **kwargs)
                return result
            re_handler = re.compile(handler)
            self._pre_handlers.append((re_handler, Conversation(func)))
            return wraps(func)(_decorator)

        return _outer_decorator

    def handler(self, handler=None):
        def _outer_decorator(func):
            def _decorator(*args, **kwargs):
                result = func(*args, **kwargs)
                return result
            re_handler = re.compile(handler)
            self._handlers.append((re_handler, func))
            return wraps(func)(_decorator)
        return _outer_decorator

    def set_exit_button(self, exit_button):
        self._exit_reply_button = exit_button

    def send_message(self, chat_id, text, reply_markup=None):
        if chat_id in self._conversations:
            new_reply_markup = utils.ReplyKeyboardMarkup()
            new_reply_markup.append_buttons(self._exit_reply_button)
            api.send_message(self.token, chat_id=chat_id, text=text, reply_markup=new_reply_markup)
        elif reply_markup is not None:
            reply_markup.append_buttons(self._exit_reply_button)
            api.send_message(self.token, chat_id=chat_id, text=text, reply_markup=reply_markup)
        else:
            api.send_message(self.token, chat_id=chat_id, text=text)

    def set_webhook(self, url=None, certificate=None):
        return api.set_webhook(self.token, url, certificate)

    def delete_webhook(self):
        return api.delete_webhook(self.token)

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








