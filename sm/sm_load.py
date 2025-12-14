import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()
res = cur.execute("SELECT enemies FROM data")
res.fetchone()