 #   ____                    _____           _       _     _       _
 #  / __ \                  / ____|         | |     | |   | |     | |
 # | |  | |_ __   ___ _ __ | (___  ___  __ _| | ____| | __| | ___ | | __
 # | |  | | '_ \ / _ | '_ \ \___ \/ __|/ _` | |/ / _` |/ _` |/ _ \| |/ /
 # | |__| | |_) |  __| | | |____) \__ | (_| |   | (_| | (_| | (_) |   < 
 #  \____/| .__/ \___|_| |_|_____/|___/\__,_|_|\_\__,_|\__,_|\___/|_|\_\
 #        | |
 #        |_|                                        by Level ASMer

import os
import twitchircpy
import deform
import sqlite3
import time
import commands
import db
from random import random
from wsgiref.simple_server import make_server
from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator
from pyramid.response import Response

DATABASE = "./ssakdook.db"
bot = twitchircpy.Bot(os.environ['OAUTH'], os.environ['NICKNAME'], "!", os.environ['NICKNAME'], True)

def timer():
    con = sqlite3.connect(DATABASE)
    c = con.cursor()
    for x in c.execute('SELECT id, description, cooltime, latest_use FROM timers'):
        if x is not None:
            if time.time() > (float(x[2]) * 60) + float(x[3]):
                c.execute('UPDATE timers SET latest_use=? WHERE id=?', (time.time(), x[0], ))
                con.commit()
                con.close()
                return x[1]
    con.close()
    return ''

@bot.event
def on_connect():
    db.createdb()
    print("Connected!")

@bot.event
def on_message(message):
    parse_context = message.content
    parse_command = ''
    if commands.getcommand(parse_context) is not None:
        if commands.getcommand(parse_context) in parse_context:
            parse_command = commands.getcommand(parse_context)
            bot.send_message(message.channel, commands.convertvalue(parse_command, message))
    bot.send_message(message.channel, timer())

bot.start_timed_messages()
bot.start()

if __name__ == '__main__':
    with Configurator() as config:
        session_factory = SignedCookieSessionFactory('deletebrig!')
        config.set_session_factory(session_factory)
        config.include('pyramid_chameleon')
        deform.renderer.configure_zpt_renderer()
        config.add_static_view(name='static', path='static/')
        config.add_route('home', '/')
        config.add_route('command', '/command/list/{id}')
        config.add_route('command_add', '/command/add')
        config.add_route('command_edit', '/command/edit/{id}')
        config.add_route('command_delete', '/command/delete/{id}')
        config.add_route('timer', '/timer/list/{id}')
        config.add_route('timer_add', '/timer/add')
        config.add_route('timer_edit', '/timer/edit/{id}')
        config.add_route('timer_delete', '/timer/delete/{id}')
        config.add_route('filter', '/filter/list/{id}')
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()