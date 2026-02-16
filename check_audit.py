import sqlite3

db_path = r"C:\InfinityMesh\memory\state\memory.db"

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM audit WHERE action='nats_route'")
count = c.fetchone()[0]

print("Audit rows:", count)

conn.close()
