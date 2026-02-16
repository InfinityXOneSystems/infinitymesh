import sqlite3
import time

db = r"C:\InfinityMesh\memory\state\memory.db"

conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS heartbeat(ts TEXT)")
c.execute("SELECT COUNT(*) FROM heartbeat")
first = c.fetchone()[0]
conn.close()

time.sleep(5)

conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM heartbeat")
second = c.fetchone()[0]
conn.close()

print(first, second)
