import subprocess
import time

while True:
    subprocess.run(["docker","ps"])
    time.sleep(30)
