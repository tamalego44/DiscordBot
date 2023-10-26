import sqlite3
import time
import os

#TODO: Encapsulate
db_path = "habiba2.db"
con = sqlite3.connect(db_path)

def createDB():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history(server, filename, time, name, uploader)")

def insert(server, filename, name, uploader):
    t = time.time()
    cur = con.cursor()
    data = (server, filename, t, name, uploader)
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