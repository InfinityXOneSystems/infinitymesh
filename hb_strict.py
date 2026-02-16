import sqlite3, time
db = r"C:\InfinityMesh\memory\state\memory.db"

conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM heartbeat")
first = c.fetchone()[0]
conn.close()

time.sleep(6)

conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM heartbeat")
second = c.fetchone()[0]
conn.close()

print(first, second)
