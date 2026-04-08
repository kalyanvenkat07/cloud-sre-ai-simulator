from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from inference import run_inference
from datetime import datetime

app = FastAPI(title="🚀 Cloud SRE AI Simulator")

# ---------------- STATE ----------------
system_state: Dict = {
    "services": {
        "web": "running",
        "db": "running",
        "cache": "running"
    },
    "incidents": [],
    "metrics": {
        "failures": 0,
        "recoveries": 0
    }
}

# ---------------- MODEL ----------------
class Command(BaseModel):
    command: str
    target: str

# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Cloud SRE Simulator Running 🚀"}

@app.get("/state")
def get_state():
    return system_state

@app.post("/reset")
def reset():
    global system_state
    system_state = {
        "services": {
            "web": "running",
            "db": "running",
            "cache": "running"
        },
        "incidents": [],
        "metrics": {
            "failures": 0,
            "recoveries": 0
        }
    }
    return {"status": "System reset successful"}

@app.post("/step")
def step(cmd: Command):
    service = cmd.target

    if service not in system_state["services"]:
        return {"error": "Invalid service"}

    # ---------------- SIMULATION ----------------
    if cmd.command == "fail":
        system_state["services"][service] = "failed"
        system_state["metrics"]["failures"] += 1

    elif cmd.command == "restart":
        system_state["services"][service] = "running"
        system_state["metrics"]["recoveries"] += 1

    elif cmd.command == "stop":
        system_state["services"][service] = "stopped"

    else:
        return {"error": "Invalid command"}

    # ---------------- INCIDENT LOG ----------------
    system_state["incidents"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "action": cmd.command,
        "service": service
    })

    # ---------------- AI ----------------
    ai_output = run_inference(cmd.command, cmd.target)

    return {
        "message": f"{cmd.command} executed on {service}",
        "state": system_state,
        "ai": ai_output
    }
