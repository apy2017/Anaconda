from technobot import TechnoBot
from technobot import database
import config

bot = TechnoBot(config.token, ignore_old=True, timeout=1)


@bot.conversation(handler='Выбрать опрос')
def poll_coroutine(init_message):
    chat_id = init_message.chat.id
    pole_is_chosen = False
    bot.send_message(chat_id, 'Введите название опроса:')
    while not pole_is_chosen:
        message = yield
        pole_is_chosen = database.db_get_poll(message.text)
        if not pole_is_chosen:
            bot.send_message(chat_id, 'Нет опроса с таким кодом, попробуйте еще.')
    question_list = database.db_get_questions(pole_is_chosen.id)
    questions = [question for question in question_list]
    for question in questions:
        bot.send_message(chat_id, question.caption)
        message = yield
        database.db_add_answer(question, message.text)

if __name__ == '__main__':
    bot.polling()