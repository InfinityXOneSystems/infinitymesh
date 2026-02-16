import sqlite3
conn = sqlite3.connect(r"C:\InfinityMesh\memory\state\memory.db")
c = conn.cursor()
c.execute("INSERT INTO sessions VALUES ('test','now')")
conn.commit()
c.execute("SELECT * FROM sessions WHERE id='test'")
row = c.fetchone()
conn.close()
if not row:
    raise Exception("Memory write/read failed")
print("MEMORY_OK")
