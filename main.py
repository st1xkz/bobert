import os
from keep_alive import keep_alive

my_secret = os.environ["TOKEN"]

from bobert import bot

keep_alive()