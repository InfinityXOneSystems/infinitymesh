import os
import json
import time
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

ROOT = r"C:\InfinityMesh"
TREE_JSON = r"C:\InfinityMesh\memory\state\tree_state.json"
DB_PATH = r"C:\InfinityMesh\memory\state\memory.db"

EXCLUDE = {
    "node_modules", ".venv", "venv",
    "__pycache__", ".git", ".cache",
    "dist", "build"
}

def build_tree(start_path):
    tree = {}
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        rel_path = os.path.relpath(root, start_path)
        if rel_path == ".":
            current = tree
        else:
            parts = rel_path.split(os.sep)
            current = tree
            for p in parts:
                current = current.setdefault(p, {})
        for d in dirs:
            current[d] = {}
        for f in files:
            current[f] = "file"
    return tree

def persist_tree(tree):
    with open(TREE_JSON, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tree_snapshots(ts TEXT)")
    c.execute("INSERT INTO tree_snapshots VALUES (datetime('now'))")
    conn.commit()
    conn.close()

def monitor():
    last_snapshot = None
    while True:
        tree = build_tree(ROOT)
        snapshot = json.dumps(tree)
        if snapshot != last_snapshot:
            persist_tree(tree)
            last_snapshot = snapshot
        time.sleep(5)

class TreeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/tree":
            if os.path.exists(TREE_JSON):
                with open(TREE_JSON, "r", encoding="utf-8") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode())
            else:
                self.send_response(404)
                self.end_headers()

def start_server():
    server = HTTPServer(("localhost", 7778), TreeHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=monitor, daemon=True).start()
    start_server()
