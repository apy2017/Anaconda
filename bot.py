import config
import telebot

bot = telebot.TeleBot(config.token)

class Bot(TelegramObject):
    """
    Атрибуты:
        id (int): идентификатор бота.
        username (str): TechnoparkMail_bot
        name (str):  @TechnoparkMail_bot
    Аргументы:
        token (str): 342067339:AAFsQBcm8NJjUx8RtJBIlusAyREpSImf0PU
    """



 # функции бота

if __name__ == '__main__': 
     bot.polling(none_stop=True) #бесконечный цикл получения новых записей со стороны Telegram
