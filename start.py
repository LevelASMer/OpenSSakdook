import os
import twitchircpy
import sqlite3
import commands
from random import random

bot = twitchircpy.Bot(os.environ['OAUTH'], os.environ['NICKNAME'], "!", os.environ['NICKNAME'], True)

@bot.event
def on_connect():
    commands.createdb()
    print("Connected!")

@bot.event
def on_message(message):
    parse_context = message.content
    parse_command = ''
    if commands.getcommand(parse_context) != None:
        if commands.getcommand(parse_context) in parse_context:
            parse_command = commands.getcommand(parse_context)
            bot.send_message(message.channel, commands.convertvalue(parse_command, message))

@bot.event
def on_sub(sub):
    bot.send_message(sub.channel, f"Thank you @{sub.login} for subbing!")

bot.start()