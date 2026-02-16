import sqlite3
conn = sqlite3.connect(r"C:\InfinityMesh\memory\state\memory.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS sessions(id TEXT, created_at TEXT)")
c.execute("INSERT INTO sessions VALUES ('exec_test','now')")
conn.commit()
c.execute("SELECT * FROM sessions WHERE id='exec_test'")
row = c.fetchone()
conn.close()
if not row:
    raise Exception("Memory execution failed")
print("MEMORY_OK")
