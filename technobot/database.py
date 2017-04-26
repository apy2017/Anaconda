from peewee import *
from datetime import datetime
from uuid import uuid3
import os

DB_NAME = 'db/bot.db'
#db = MySQLDatabase(database=...)
db = SqliteDatabase(DB_NAME)


def db_session(query_func):
    def decorate(*argc, **kwargs):
        if db.is_closed():
            db.connect()
        result = query_func(*argc, **kwargs)
        if not db.is_closed():
            db.close()
        return result
    return decorate


class User(Model):
    name = CharField()
    last_name = CharField(null=True)
    telegram_id = IntegerField()
    registration_date = DateTimeField()

    class Meta:
        database = db


class Poll(Model):
    owner = ForeignKeyField(User, related_name='owner')
    poll_id = CharField()
    name = CharField()
    starts_number = IntegerField()
    date_created = DateTimeField()

    class Meta:
        database = db


class Question(Model):
    poll = ForeignKeyField(Poll, related_name='poll')
    caption = CharField()
    data_type = CharField()

    class Meta:
        database = db


class Answer(Model):
    question = ForeignKeyField(Question, related_name='question')
    caption = CharField()

    class Meta:
        database = db


@db_session
def _is_account_exist(telegram_id):
    client = User.select().where(User.telegram_id == telegram_id)
    if client.exists():
        return True
    return False


@db_session
def _is_poll_exist(poll_id):
    poll = Poll.select().where(Poll.poll_id == poll_id)
    if poll.exists():
        return True
    return False


@db_session
def db_register_user(telegram_id, name, last_name):
    if not (_is_account_exist(telegram_id)):
        user = User(telegram_id=telegram_id, name=name, last_name=last_name, registration_date=datetime.now())
        user.save()
        return True
    return False


@db_session
def db_get_user(telegram_id):
    user = User.select().where(User.telegram_id == telegram_id)
    if user.exists():
        return user.first()
    return False


@db_session
def db_create_poll(poll_id, user, name):
    if not(_is_poll_exist(poll_id)):
        poll = Poll(owner_id=user, poll_id=poll_id, name=name, starts_number=0, date_created=datetime.now())
        poll.save()
        return poll
    return False


@db_session
def db_get_poll(poll_id):
    poll = Poll.select().where(Poll.poll_id == poll_id)
    if poll.exists():
        return poll.first()
    return False


@db_session
def db_get_questions(poll_id):
    questions = Question.select().where(Question.poll_id == poll_id)
    if questions.exists():
        return questions
    return False


@db_session
def db_add_question(poll, caption, data_type):
    question = Question(poll_id = poll, caption=caption, data_type=data_type)
    question.save()
    return question


@db_session
def db_add_answer(question, answer):
    answer = Answer(question=question, caption=answer)
    answer.save()
    return answer

def setup():
    if not(os.path.isfile(DB_NAME)):
        User.create_table()
        Poll.create_table()
        Question.create_table()
        Answer.create_table()


if __name__ == '__main__':
    setup()

