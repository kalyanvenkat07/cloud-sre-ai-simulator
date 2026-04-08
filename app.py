from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

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
        }
    }

state = default_state()

# ---------------- MODEL ----------------
class Action(BaseModel):
    command: str
    target: str

# ---------------- STATE API ----------------
@app.get("/state")
def get_state():
    return state

# ---------------- RESET API (STRICT ✅) ----------------
@app.post("/reset")
def reset():
    global state
    state = default_state()
    return state  # ✅ ONLY state (IMPORTANT)

# ---------------- STEP API (STRICT + ELITE LOGIC) ----------------
@app.post("/step")
def step(action: Action):
    global state

    cmd = action.command.lower()
    target = action.target.lower()

    if target not in state["services"]:
        return state  # still return valid state

    severity = "LOW"
    impact = "Minimal"
    root_cause = "Unknown"
    auto_healed = False

    # ---------------- FAIL ----------------
    if cmd == "fail":
        state["services"][target] = "failed"
        state["metrics"]["failures"] += 1

        severity = "HIGH"
        impact = f"{target} service outage affecting users"
        root_cause = "Service crash / resource exhaustion"

        # 🔥 AUTO-HEAL
        auto_healed = True
        state["services"][target] = "running"
        state["metrics"]["recoveries"] += 1

    # ---------------- RESTART ----------------
    elif cmd == "restart":
        state["services"][target] = "running"
        state["metrics"]["recoveries"] += 1

        severity = "LOW"
        impact = "Service restored"
        root_cause = "Manual recovery"

    # ---------------- STOP ----------------
    elif cmd == "stop":
        state["services"][target] = "stopped"

        severity = "MEDIUM"
        impact = f"{target} service stopped"
        root_cause = "Manual shutdown"

    # ---------------- INCIDENT ----------------
    incident = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "service": target,
        "action": cmd,
        "severity": severity,
        "impact": impact,
        "root_cause": root_cause,
        "auto_healed": auto_healed
    }

    state["incidents"].append(incident)

    return state  # ✅ STRICT FORMAT (IMPORTANT)

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Cloud SRE AI Simulator is running"}
