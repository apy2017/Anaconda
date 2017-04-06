from peewee import *
from datetime import datetime
import os

DB_NAME = 'db/bot.db'
#db = MySQLDatabase(database=...)
db = SqliteDatabase(DB_NAME)


def db_session(query_func):
    def decorate(*argc):
        if db.is_closed():
            db.connect()
        result = query_func(*argc)
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


@db_session
def _is_account_exist(telegram_id):
    client = User.select().where(User.telegram_id == telegram_id)
    if client.exists():
        return True
    return False


@db_session
def db_register_user(telegram_id, name, last_name):
    if not (_is_account_exist(telegram_id)):
        user = User(telegram_id=telegram_id, name=name, last_name=last_name, registration_date=datetime.now())
        user.save()
        return True
    return False


def setup():
    if not(os.path.isfile(DB_NAME)):
        User.create_table()


if __name__ == '__main__':
    setup()

