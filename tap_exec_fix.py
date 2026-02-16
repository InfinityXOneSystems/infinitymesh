import sqlite3, datetime
conn = sqlite3.connect(r"C:\InfinityMesh\memory\state\memory.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS audit(id TEXT, action TEXT, timestamp TEXT)")
c.execute("INSERT INTO audit VALUES ('exec_validation','mesh_exec', ?)",
          (datetime.datetime.utcnow().isoformat(),))
conn.commit()
conn.close()
print("TAP_OK")
