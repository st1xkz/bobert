import os

my_secret = os.environ['TOKEN']

from bobert import bot

bot.bot.run()
