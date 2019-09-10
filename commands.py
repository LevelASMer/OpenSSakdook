# Default Commands
import os
import sqlite3
import time
from random import random
from twitch import TwitchClient

client = TwitchClient(os.environ['CLIENT_ID'], os.environ['TOKEN'])

DATABASE = './ssakdook.db'

def convertvalue(command, arg):
    com = (command,)
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    c.execute('SELECT command, description, cooltime FROM commands WHERE command = ?', com)
    fetch = c.fetchone()
    con.close()

    convert = ''

    if "$percent" in fetch[1]: convert = fetch[1].replace("$percent", getpercent())
    if "$time" in fetch[1]: convert = fetch[1].replace("$time", gettime())
    if "$nick" in fetch[1]: convert = fetch[1].replace("$nick", arg.user)
    if "$channel" in fetch[1]: convert = fetch[1].replace("$channel", arg.channel)
    if "$followers" in fetch[1]: convert = fetch[1].replace("$followers", getfollowers(arg.channel))
    if "$subscriberCount" in fetch[1]: convert = fetch[1].replace("$subscriberCount", getsubscribers(arg.channel))
    return convert

def getcommand(context):
    split = context.split(" ")
    for x in split:
        com = (x,)
        con = sqlite3.connect(DATABASE)
        c = con.cursor()

        c.execute('SELECT command FROM commands WHERE command = ?', com)
        value = c.fetchone()
        con.close()
        if value != None:
            return value[0]

def getsubscribers(userid):
    channel = client.search.channels(userid, limit=1, offset=0)[0]
    try:
        info = client.channels.get_subscribers(channel['id'], limit=1, offset=0)
        return str(info[0]['_total'])
    except:
        return str("0")

def gettitle(userid):
    channel = client.search.channels(userid, limit=1, offset=0)[0]
    if channel is None:
        return str("")
    return str(channel['status'])

def getgame(userid):
    channel = client.search.channels(userid, limit=1, offset=0)[0]
    if channel is None:
        return str("")
    return str(channel['game'])

def getfollowers(userid):
    channel = client.search.channels(userid, limit=1, offset=0)[0]
    return str(channel['followers'])

def gettotalview(userid):
    channel = client.search.channels(userid, limit=1, offset=0)[0]
    return str(channel['views'])

def gettime():
    now = time.gmtime(time.time())
    return "{}년 {}월 {}일 {}시 {}분 {}초".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

def getpercent():
    per1 = round(random() * 100) % 10
    per2 = 0 if per1 == 10 else round(random() * 10) % 10
    result = (str(per1) if per1 > 0 else "") + str(per2) + "." + (str(round(random() * 100) % 100) if per1 != 10 else "00") + "%"

    return result