import sqlite3
import time

#TODO: Encapsulate
con = sqlite3.connect("habiba.db")
#TODO: if db doesnt exist create it
def createDB():
    cur = con.cursor()
    cur.execute("CREATE TABLE history(server, filename, time, name)")

def insert(server, filename):
    t = time.time()
    cur = con.cursor()
    data = (server, filename, t)
    cur.execute("INSERT INTO history VALUES(?, ?, ?)", data)
    con.commit()

def get(server, index=-1):
    print(server)
    cur = con.cursor()
    data = [server]
    data = cur.execute("SELECT * from history WHERE server=? ORDER BY time ASC", data)
    return data.fetchall()[index]


#insert("servername", "filename2")

print(get("639621895926579211"))