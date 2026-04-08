from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from inference import run_inference

app = FastAPI()

# ----------------------------
# Global State
# ----------------------------
state = {
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

# ----------------------------
# Request Model
# ----------------------------
class CommandRequest(BaseModel):
    command: str
    target: str

# ----------------------------
# Get Current State
# ----------------------------
@app.get("/state")
def get_state():
    return state


@app.post("/reset")
def reset_env():
    global state

    state = {
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

    return {
        "status": "reset successful",
        "state": state
    }

# ----------------------------
# Execute Command
# ----------------------------
@app.post("/step")
def step(req: CommandRequest) -> Dict[str, Any]:
    global state

    command = req.command.lower()
    target = req.target.lower()

    # Log incident
    state["incidents"].append(f"{command} on {target}")

    # Apply command logic
    if command == "fail":
        state["services"][target] = "failed"
        state["metrics"]["failures"] += 1

    elif command == "restart":
        state["services"][target] = "running"
        state["metrics"]["recoveries"] += 1

    elif command == "stop":
        state["services"][target] = "stopped"

    # Call AI inference
    ai_response = run_inference(command, target)

    return {
        "message": "step executed",
        "ai_response": ai_response,
        "state": state
    }



@app.get("/")
def root():
    return {"message": "Cloud SRE AI Simulator is running"}
