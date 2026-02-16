import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import os
import time
import sqlite3
import datetime
import json

ROOT = r"C:\InfinityMesh"
ROUTER_PATH = r"C:\InfinityMesh\core\router\router.py"
DB_PATH = r"C:\InfinityMesh\memory\state\memory.db"
LOG_PATH = r"C:\InfinityMesh\logs\router.log"
PYTHON_EXE = r"C:\Users\JARVIS\AppData\Local\Programs\Python\Python311\python.exe"

os.chdir(ROOT)

def ensure_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS heartbeat(ts TEXT)")
    conn.commit()
    conn.close()

class InfinityMeshService(win32serviceutil.ServiceFramework):
    _svc_name_ = "InfinityMeshRouter"
    _svc_display_name_ = "InfinityMesh Event Router"
    _svc_description_ = "InfinityMesh Self-Healing Router Supervisor"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def log(self, message, level="INFO"):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": level,
            "message": message
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def heartbeat(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO heartbeat VALUES (?)",
                  (datetime.datetime.utcnow().isoformat(),))
        conn.commit()
        conn.close()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log("Service stopping")
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        self.log("Supervisor starting")
        ensure_tables()

        while True:
            self.log("Launching router child")

            self.process = subprocess.Popen(
                [PYTHON_EXE, ROUTER_PATH],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.log(f"Router PID: {self.process.pid}")

            while True:
                if win32event.WaitForSingleObject(self.stop_event, 5000) == win32event.WAIT_OBJECT_0:
                    self.log("Stop event received")
                    return

                if self.process.poll() is not None:
                    stdout, stderr = self.process.communicate()
                    self.log(f"Router exited code {self.process.returncode}", "ERROR")
                    self.log(f"STDOUT: {stdout}", "ERROR")
                    self.log(f"STDERR: {stderr}", "ERROR")
                    break

                self.heartbeat()

            time.sleep(2)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(InfinityMeshService)
