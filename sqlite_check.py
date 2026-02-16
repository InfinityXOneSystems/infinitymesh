import sqlite3
conn = sqlite3.connect(r"C:\InfinityMesh\memory\state\memory.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS audit(id TEXT, action TEXT, timestamp TEXT)")
c.execute("INSERT INTO audit VALUES ('validator','system_check','now')")
conn.commit()
conn.close()
print("OK")
