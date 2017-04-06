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