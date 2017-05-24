import json
import copy

class User:
    def __init__(self, answer_dict):
        self.id = int(answer_dict['id'])
        self.first_name = answer_dict['first_name']
        self.last_name = answer_dict.get('last_name')
        self.username = answer_dict.get('username')


class Chat(User):
    def __init__(self, answer_dict):
        super().__init__(answer_dict)
        self.type = answer_dict['type']
        self.title = answer_dict.get('title')
        self.all_members_are_administrators = answer_dict.get('all_members_are_administrators')


class Message:
    def __init__(self, answer_dict):
        self.message_id = answer_dict['message_id']
        self.from_user = User(answer_dict['from']) if 'from' in answer_dict else None
        self.date = answer_dict['date']
        self.chat = Chat(answer_dict['chat'])
        self.text = answer_dict['text'] if 'text' in answer_dict else None


class Update:
    def __init__(self, answer_dict):
        self.update_id = answer_dict['update_id']
        self.message = Message(answer_dict['message']) if 'message' in answer_dict else None


class ConvertibleJson:
    @property
    def json(self):
        #props = {key: self.__dict__[key] for key in self.__dict__ if self.__dict__[key] is not None}
        return json.dumps(self, default=lambda o: o.__dict__)


class ReplyKeyboardMarkup(ConvertibleJson):
    def __init__(self, keyboard=None, resize_keyboard=True, one_time_keyboard=False, selective=False):
        self.keyboard = keyboard if keyboard is not None else [[]]
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        super().__init__()

    def append_buttons(self, *args):
        for button in args:
            if [button] not in self.keyboard:
                self.keyboard.append([button])


class KeyboardButton(ConvertibleJson):
    def __init__(self, text=None, request_contact=False, request_location=False):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        super().__init__()




