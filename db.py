# Default Commands
import sqlite3
import time

DATABASE = './ssakdook.db'

def createdb():
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY AUTOINCREMENT, command TEXT, description TEXT, cooltime INTEGER)')
        c.execute('CREATE TABLE IF NOT EXISTS timers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, cooltime INTEGER)')
        c.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, description TEXT, date TEXT)')
        c.execute('CREATE UNIQUE INDEX IF NOT EXISTS pk_commands ON "commands"("id","command")')
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!per', '확률: $percent', 5)")
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!time', '현재 시간: $time', 5)")
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!bbang', '$nick 으악', 5)")
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!channel', '현재 채널: $channel', 5)")
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!followers', '현재 이 채널의 팔로워: $followers', 5)")
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!title', '이 채널의 제목: $title', 5)")
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!views', '이 채널의 총 시청자: $views', 5)")
        # c.execute("INSERT OR IGNORE INTO commands VALUES('!subscriber', '이 채널의 총 구독자: $subscriberCount', 5)")
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