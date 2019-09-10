# Default Commands
import sqlite3
import time

DATABASE = './ssakdook.db'

def createdb():
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY AUTOINCREMENT, command TEXT, description TEXT, cooltime INTEGER, latest_use TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS timers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, cooltime INTEGER)')
        c.execute('CREATE UNIQUE INDEX IF NOT EXISTS pk_commands ON "commands"("id","command")')
        con.commit()
    except con.Error as e:
        print(e)
    finally:
        con.close()

def savelog(user, content):
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        values = (user, content)
        c.execute("INSERT INTO logs (username, description, date) VALUES(?, ?, datetime('now'))", values,)
        con.commit()
    except con.Error as e:
        print(e)
    finally:
        con.close()