import sqlite3
import time
import os
from util import Song

#TODO: Encapsulate
db_path = "habiba2.db"
con = sqlite3.connect(db_path)

def createDB():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history(server, filename, time, name, uploader)")

def insert(server, song_obj: Song):
    t = time.time()
    cur = con.cursor()
    data = (server, song_obj.filename, t, song_obj.name, song_obj.uploader.id)
    print(song_obj.filename)
    print(type(song_obj.filename))
    cur.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", data)
    con.commit()

def get(server, index=-1):
    print(server)
    cur = con.cursor()
    data = [server]
    data = cur.execute("SELECT * from history WHERE server=? ORDER BY time ASC", data)
    return data.fetchall()[index]

#if DB doesn't exist; create it
createDB()

if __name__ == "__main__":
    #insert("servername", "filename2")

    # print(get("639621895926579211"))
    insert("639621895926579211", "test.mp3", "Test Song", 123456789)