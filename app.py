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

# ---------------- RESET API ----------------
@app.post("/reset")
def reset():
    global state
    state = default_state()
    return {"status": "reset successful", "state": state}

# ---------------- STEP API ----------------
@app.post("/step")
def step(action: Action):
    global state

    cmd = action.command.lower()
    target = action.target.lower()

    if target not in state["services"]:
        return {"error": "Invalid service"}

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

    else:
        return {"error": "Invalid command"}

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

    # ---------------- AI RESPONSE ----------------
    ai_response = f"""
🚨 Incident Report
Service: {target}
Severity: {severity}

Impact:
{impact}

Root Cause:
{root_cause}

Auto-Healing:
{"Executed" if auto_healed else "Not triggered"}

Recommended Actions:
- Monitor logs
- Ensure stability
"""

    return {
        "state": state,
        "ai_response": ai_response,
        "incident": incident
    }

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Cloud SRE AI Simulator is running"}
