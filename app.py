from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from inference import run_inference

app = FastAPI()

# ----------------------------
# Global State
# ----------------------------
def get_initial_state():
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

state = get_initial_state()

# ----------------------------
# Request Model
# ----------------------------
class CommandRequest(BaseModel):
    command: str
    target: str

# ----------------------------
# Root
# ----------------------------
@app.get("/")
def root():
    return {"message": "Cloud SRE AI Simulator is running"}

# ----------------------------
# Get State
# ----------------------------
@app.get("/state")
def get_state():
    return state

# ----------------------------
# Reset (VERY IMPORTANT)
# ----------------------------
@app.post("/reset")
def reset_env():
    global state
    state = get_initial_state()
    return {
        "status": "reset successful",
        "state": state
    }

# ----------------------------
# Execute Step
# ----------------------------
@app.post("/step")
def step(req: CommandRequest) -> Dict[str, Any]:
    global state

    command = req.command.lower()
    target = req.target.lower()

    # ----------------------------
    # Validate target
    # ----------------------------
    if target not in state["services"]:
        return {"error": f"Invalid service: {target}"}

    # ----------------------------
    # Apply command
    # ----------------------------
    if command == "fail":
        state["services"][target] = "failed"
        state["metrics"]["failures"] += 1

    elif command == "restart":
        state["services"][target] = "running"
        state["metrics"]["recoveries"] += 1

    elif command == "stop":
        state["services"][target] = "stopped"

    else:
        return {"error": f"Invalid command: {command}"}

    # ----------------------------
    # Add structured incident ✅ FIXED
    # ----------------------------
    state["incidents"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "action": command,
        "service": target
    })

    # ----------------------------
    # AI Inference
    # ----------------------------
    ai_response = run_inference(command, target)

    # ----------------------------
    # Response
    # ----------------------------
    return {
        "message": "step executed",
        "ai_response": ai_response,
        "state": state
    }
