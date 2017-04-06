from technobot import TechnoBot
from technobot import database
import config

bot = TechnoBot(config.token, timeout=1)
bot.polling()