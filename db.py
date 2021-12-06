import sqlite3

import string
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect("pgn.db", check_same_thread=False)
connMultiplayer = sqlite3.connect('D:\\CLOUD\\Schaken-Multiplayer\\multiplayer.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursorMultiplayer = connMultiplayer.cursor()


def getPlayerGames(name):
    results = cursor.execute("select * from rooms where playerBlack= '"+name+"' or playerWhite ='"+name+"'").fetchall()
    games = [dict(row) for row in results]
    print(games)
    return games


def getRoomInfo(name):
    room = cursor.execute("select Name from Rooms where Name = '" + name + "'").fetchone()
    if room == None:
        return None
    else:
        return room[0]


def makeNewRoom(name):
    game = cursorMultiplayer.execute("select game from Rooms where name ='" + name + "'").fetchone()
    playerBlack = cursorMultiplayer.execute("select id from Players where room = '"+name+"' and Color = 'b'").fetchone()
    playerWhite = cursorMultiplayer.execute("select id from Players where room = '"+name+"' and Color = 'w'").fetchone()
    print(playerBlack[0])
    print(playerWhite[0])
    cursor.execute("insert into rooms values (?,?,?,?)", (name, game[0], playerBlack[0], playerWhite[0]))
    conn.commit()

def updateRoom(name):
    games = cursorMultiplayer.execute("select game from Rooms where name ='" + name + "'").fetchone()
    game = games[0]
    cursor.execute("update rooms set game='" + game + "' where name is '" + name + "'")
    conn.commit()

def getRoomGame(name):
    game = cursor.execute("select game from Rooms where name is '" + name + "'").fetchone()
    if game == None:
        return None
    return game[0]
