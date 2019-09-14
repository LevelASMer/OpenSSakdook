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
from openssakdook import commands
from openssakdook import db
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

def main(global_config, **settings):
    config = Configurator(settings=settings)
    session_factory = SignedCookieSessionFactory('deletebrig!')
    config.set_session_factory(session_factory)
    config.include('pyramid_chameleon')
    config.scan('.views')
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
    config.add_route('word_add', '/filter/add_word')
    config.add_route('word_edit', '/filter/edit_word/{id}')
    config.add_route('word_delete', '/filter/delete_word/{id}')
    config.add_route('url_add', '/filter/add_url')
    config.add_route('url_edit', '/filter/edit_url/{id}')
    config.add_route('url_delete', '/filter/delete_url/{id}')
    deform.renderer.configure_zpt_renderer()
    bot.start_timed_messages()
    bot.start()
    return config.make_wsgi_app()