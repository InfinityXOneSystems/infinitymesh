import sqlite3
conn = sqlite3.connect(r"C:\InfinityMesh\memory\state\memory.db")
c = conn.cursor()
c.execute("SELECT * FROM audit WHERE action='nats_route'")
row = c.fetchone()
conn.close()
if not row:
    raise Exception("Mesh event not processed")
print("MESH_OK")
