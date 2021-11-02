import customutils as cu
con = cu.openDB()
cur = con.cursor()
ID = 1
cur.execute(f"select x, y, waitTime,maxPeople from RIDE where ID = {ID};")
res = cur.fetchone()
con.close()
print([res[0],res[1]],res[2],res[3])