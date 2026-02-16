import sqlite3, datetime

db_path = r"C:\InfinityMesh\memory\state\memory.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS sessions(id TEXT, created_at TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS responses(id TEXT, content TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS audit(id TEXT, action TEXT, timestamp TEXT)")

c.execute("INSERT INTO audit VALUES (?, ?, ?)",
          ("validation", "system_check", datetime.datetime.utcnow().isoformat()))

conn.commit()
conn.close()

print("SQLITE_OK")
