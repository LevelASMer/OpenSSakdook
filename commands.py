# Default Commands
import sqlite3
import time
from random import random

DATABASE = './ssakdook.db'

def createdb():
    try:
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS commands (command text PRIMARY KEY, description text, cooltime int)')
        c.execute("INSERT OR IGNORE INTO commands VALUES('!per', '확률: $percent', 5)")
        c.execute("INSERT OR IGNORE INTO commands VALUES('!time', '현재 시간: $time', 5)")
        c.execute("INSERT OR IGNORE INTO commands VALUES('!bbang', '$nick 으악', 5)")
        con.commit()
    except con.Error as e:
        print(e)
    finally:
        con.close()

def convertvalue(command, arg):
    com = (command,)
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    c.execute('SELECT * FROM commands WHERE command = ?', com)
    fetch = c.fetchone()
    con.close()

    convert = ''

    if "$percent" in fetch[1]: convert = fetch[1].replace("$percent", getpercent())
    if "$time" in fetch[1]: convert = fetch[1].replace("$time", gettime())
    if "$nick" in fetch[1]: convert = fetch[1].replace("$nick", arg.user)
    if "$channel" in fetch[1]: convert = fetch[1].replace("$channel", arg.channel)
    return convert

def getcommand(context):
    split = context.split(" ")
    for x in split:
        com = (x,)
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        c.execute('SELECT command FROM commands WHERE command = ?', com)
        value = c.fetchone()
        if value != None:
            con.close()
            return value[0]

def gettime():
    now = time.gmtime(time.time())
    return "{}년 {}월 {}일 {}시 {}분 {}초".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

def getpercent():
    per1 = round(random() * 100) % 10
    per2 = 0 if per1 == 10 else round(random() * 10) % 10
    result = (str(per1) if per1 > 0 else "") + str(per2) + "." + (str(round(random() * 100) % 100) if per1 != 10 else "00") + "%"

    return result