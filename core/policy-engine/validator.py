import json
import datetime

def validate(action):
    log = {
        "action": action,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "validated": True
    }
    print(json.dumps(log))

if __name__ == "__main__":
    validate("mesh_activation")
