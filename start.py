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
import sqlite3
import deform
import commands
import db
from random import random
from wsgiref.simple_server import make_server
from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator
from pyramid.response import Response

bot = twitchircpy.Bot(os.environ['OAUTH'], os.environ['NICKNAME'], "!", os.environ['NICKNAME'], True)

@bot.event
def on_connect():
    db.createdb()
    print("Connected!")

@bot.event
def on_message(message):
    parse_context = message.content
    parse_command = ''
    db.savelog(message.user, message.content)
    if commands.getcommand(parse_context) != None:
        if commands.getcommand(parse_context) in parse_context:
            parse_command = commands.getcommand(parse_context)
            bot.send_message(message.channel, commands.convertvalue(parse_command, message))

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
        config.add_route('log', '/log/list/{id}')
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()