import sqlite3
conn = sqlite3.connect(r"C:\InfinityMesh\memory\state\memory.db")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM heartbeat")
count = c.fetchone()[0]
conn.close()
print(count)
