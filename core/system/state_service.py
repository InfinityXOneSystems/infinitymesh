from fastapi import FastAPI
import sqlite3, os, json, datetime, psutil

app = FastAPI()

DB = r"C:\InfinityMesh\memory\state\memory.db"
ROOT = r"C:\InfinityMesh"
REGISTRY = r"C:\InfinityMesh\docs\REGISTRY.json"
TODO = r"C:\InfinityMesh\docs\TODO.json"
TREE = r"C:\InfinityMesh\docs\FOLDER_TREE.json"

IGNORE = {"node_modules",".git","__pycache__","venv"}

def safe_json(path):
    if not os.path.exists(path):
        return {"error":"file_not_found","path":path}
    try:
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error":"invalid_json","message":str(e)}

def count_files():
    total = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE]
        total += len(files)
    return total

@app.get("/health")
def health():
    return {"status":"healthy","timestamp":datetime.datetime.utcnow().isoformat()}

@app.get("/heartbeat")
def heartbeat():
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS heartbeat(ts TEXT)")
        c.execute("SELECT COUNT(*) FROM heartbeat")
        count = c.fetchone()[0]
        conn.close()
        return {"heartbeat_count":count}
    except Exception as e:
        return {"error":"heartbeat_failure","message":str(e)}

@app.get("/metrics")
def metrics():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "file_count": count_files(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/tree")
def tree():
    return safe_json(TREE)

@app.get("/registry")
def registry():
    return safe_json(REGISTRY)

@app.get("/todo")
def todo():
    return safe_json(TODO)
