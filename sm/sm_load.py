import sqlite3
import sm_enemy

con = sqlite3.connect("data/data.db")
cur = con.cursor()
enemies_number = 0
query = f"SELECT COUNT(*) FROM enemies"
cur.execute(query)
row_count = cur.fetchone()[0]
lines =  int(row_count)


for i in range(0,lines,1):
    damage = cur.execute('select damage from enemies where id = 1')
    hp = cur.execute('select hp from enemies where id = 1')
    img_path = cur.execute('select img from enemies where id = 1')
    sm_enemy.sm_enemy(damage,hp,0,0,img_path)
