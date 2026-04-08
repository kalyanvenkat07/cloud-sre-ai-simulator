from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()

# ---------------- STATE ----------------
def default_state():
    return {
        "services": {
            "web": "running",
            "db": "running",
            "cache": "running"
        },
        "incidents": [],
        "metrics": {
            "failures": 0,
            "recoveries": 0
        },
        "steps": 0
    }

state = default_state()

class Action(BaseModel):
    command: str
    target: str

# ---------------- HELPERS ----------------
def log_incident(service, action, severity, impact, root_cause, auto_healed):
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "service": service,
        "action": action,
        "severity": severity,
        "impact": impact,
        "root_cause": root_cause,
        "auto_healed": auto_healed
    }

def auto_heal(state):
    for s in state["services"]:
        if state["services"][s] == "failed":
            if random.random() < 0.3:
                state["services"][s] = "running"
                state["metrics"]["recoveries"] += 1

# ---------------- ROUTES ----------------
@app.get("/")
def root():
    return {"message": "Cloud SRE Simulator Running 🚀"}

@app.get("/state")
def get_state():
    return state

@app.post("/reset")
def reset():
    global state
    state = default_state()
    return state

@app.post("/step")
def step(action: Action):
    global state

    cmd = action.command.lower()
    target = action.target.lower()

    reward = 0.0
    done = False

    if target not in state["services"]:
        return {"observation": state, "reward": {"score": -0.2}, "done": False, "info": {}}

    current = state["services"][target]

    severity = "LOW"
    impact = "Minimal"
    root_cause = "Unknown"
    auto_healed_flag = False

    if cmd == "fail":
        state["services"][target] = "failed"
        state["metrics"]["failures"] += 1
        reward -= 0.3

        severity = "HIGH"
        impact = f"{target} outage"
        root_cause = "Crash"

        if random.random() < 0.5:
            state["services"][target] = "running"
            state["metrics"]["recoveries"] += 1
            auto_healed_flag = True
            reward += 0.5

    elif cmd == "restart":
        if current == "failed":
            reward += 0.7
        else:
            reward -= 0.1

        state["services"][target] = "running"
        state["metrics"]["recoveries"] += 1

    elif cmd == "stop":
        state["services"][target] = "stopped"
        reward -= 0.25

    incident = log_incident(target, cmd, severity, impact, root_cause, auto_healed_flag)
    state["incidents"].append(incident)

    auto_heal(state)

    state["steps"] += 1

    if all(s == "running" for s in state["services"].values()):
        reward += 0.5
        done = True

    if state["steps"] >= 10:
        done = True
        reward -= 0.2

    return {
        "observation": state,
        "reward": {"score": round(reward, 2)},
        "done": done,
        "info": {}
    }
