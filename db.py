# Default Commands
import sqlite3
import time
import os

DATABASE = './ssakdook.db'

def createdb():
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY AUTOINCREMENT, command TEXT, description TEXT, cooltime INTEGER, latest_use TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS timers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, cooltime INTEGER, latest_use TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS filters_word (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS filters_link (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS settings_word (enable INTEGER, timeout INTEGER, timeout_alert INTEGER, timeout_msg TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS settings_emoticon (enable INTEGER, timeout INTEGER, emoticon_max INTEGER, timeout_alert INTEGER, timeout_msg TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS settings_symbol (enable INTEGER, timeout INTEGER, symbol_max INTEGER, timeout_alert INTEGER, timeout_msg TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS settings_repeat (enable INTEGER, timeout INTEGER, repeat_max INTEGER, timeout_alert INTEGER, timeout_msg TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS settings_link (enable INTEGER, timeout INTEGER, timeout_alert INTEGER, timeout_msg TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS settings_color (enable INTEGER, timeout INTEGER, timeout_alert INTEGER, timeout_msg TEXT)')
        c.execute('CREATE UNIQUE INDEX IF NOT EXISTS pk_commands ON "commands"("id","command")')
        con.commit()
    except con.Error as e:
        print(e)
    finally:
        con.close()

def timed(bot, timed, id):
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        c.execute('SELECT description FROM timers WHERE id=?', (id, ))
        fetch = c.fetchone()
        bot.send_message(timed.channel, fetch[0])
    except con.Error as e:
        print(e)
    finally:
        con.close()

def gettimer(bot, message):
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        for x in c.execute('SELECT id, name, description, cooltime FROM timers'):
            bot.add_timed_message(x[1], 10, os.environ['NICKNAME'], x[3] * 60, timed(bot, message, x[0]))
    except con.Error as e:
        print(e)
    finally:
        con.close()