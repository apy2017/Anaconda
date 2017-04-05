import config
import telebot

bot = telebot.TeleBot(config.token)

class Bot(TelegramObject):
    """
    Атрибуты:
        id (int): идентификатор бота.
        username (str): никнейм бота.
        name (str):  @username бота.
    Аргументы:
        token (str): Bot's unique authentication.
    """



 # функции бота

if __name__ == '__main__': 
     bot.polling(none_stop=True) #бесконечный цикл получения новых записей со стороны Telegram
