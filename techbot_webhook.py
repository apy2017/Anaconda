#!/usr/bin/env python
# -*- coding: utf-8 -*-
from technobot import TechnoBot
from technobot import database
from technobot import bot_api
from technobot.utils import KeyboardButton, ReplyKeyboardMarkup
import logging
from logging.handlers import RotatingFileHandler
from flask import request
import config
import flask
import json


app = flask.Flask(__name__)

WEBHOOK_URL = "https://{0}:{1}/".format(config.server_name, config.server_port)

bot = TechnoBot(config.token, ignore_old=True, timeout=1)

#Logging
bot_logger = bot.logger
my_handler = RotatingFileHandler('log/techbot.log', mode='a', maxBytes=5 * 1024 * 1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
my_handler.setLevel(logging.DEBUG)

bot_logger.setLevel(logging.DEBUG)
bot_logger.addHandler(my_handler)

bot.delete_webhook()
bot.set_webhook(url=WEBHOOK_URL, certificate=open(config.ssl_cert, 'r'))
exit_button = KeyboardButton(text='Выйти в главное меню')
bot.set_exit_button(exit_button)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.append_buttons(KeyboardButton(text='Выбрать опрос'))


@app.route('/lol', methods=['GET'])
def lol():
    return 'Hello world'


@app.route('/', methods=['POST'])
def index():
    if request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data()
        update = json.loads(json_string.decode())
        bot.process_webhook_update(update)
        return ''
    else:
        flask.abort(403)


@bot.conversation(handler='Выбрать опрос')
def poll_coroutine(init_message):
    chat_id = init_message.chat.id
    pole_is_chosen = False
    bot.send_message(chat_id, 'Введите код опроса:')
    poll_code = None
    while not pole_is_chosen:
        message = yield
        pole_is_chosen = bot_api.get_poll_by_code(message.text)
        if not pole_is_chosen:
            bot.send_message(chat_id, 'Нет опроса с таким кодом, попробуйте еще.')
        else:
            poll_code = message.text
    telegram_username = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
    answer_container = bot_api.add_answer_container(code=poll_code, telegram_username=telegram_username)
    questions = [(question['pk'], question['caption']) for question in pole_is_chosen]
    questions.sort(key=lambda tup: tup[0])
    for question_id, question in questions:
        bot.send_message(chat_id, question)
        message = yield
        bot_api.send_answer(question_id=question_id, answer_container_pk=answer_container['pk'], caption=message.text)
    bot.send_message(chat_id, 'Спасибо за прохождение опроса!')


@bot.handler(handler='\S+')
def start_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите действие:', reply_markup=keyboard)

if __name__ == "__main__":
        app.run()