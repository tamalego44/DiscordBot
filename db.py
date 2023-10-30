import sqlite3
import time
import os
from util import Song

#TODO: Encapsulate
db_path = "habiba.db"
con = sqlite3.connect(db_path)

def createDB():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history(server, filename, time, name, uploader)")
    cur.execute("CREATE TABLE IF NOT EXISTS money(user, balance)")

def insert_song(server, song_obj: Song):
    t = time.time()
    cur = con.cursor()
    data = (server, song_obj.filename, t, song_obj.name, song_obj.uploader.id)
    cur.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", data)
    con.commit()

def get_song(server, index=-1):
    cur = con.cursor()
    data = [server]
    data = cur.execute("SELECT * from history WHERE server=? ORDER BY time ASC", data)
    return data.fetchall()[index]

def add_money(user, amt):
    cur = con.cursor()
    data = [user]
    data = cur.execute("SELECT balance FROM money WHERE user=?", data)
    balance = data.fetchone()
    
    print(type(balance))

    if not balance:
        #user doesnt exist in DB
        data = (user, amt)
        cur.execute("INSERT INTO money VALUES(?, ?)", data)
    else:
        #user does exist in DB
        data = (amt + balance, user)
        cur.execute("UPDATE money SET balance=? WHERE user=?", data)
    
    print("done")
#if DB doesn't exist; create it
createDB()

if __name__ == "__main__":
    #insert("servername", "filename2")

    # print(get("639621895926579211"))
    # insert_song("639621895926579211", "test.mp3", "Test Song", 123456789)

    add_money("test_user", 10)