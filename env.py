import random
from datetime import datetime

MAX_STEPS = 10

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

def log_incident(state, service, action):
    state["incidents"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "service": service,
        "action": action
    })

def inject_random_failure(state):
    if random.random() < 0.2:
        service = random.choice(list(state["services"].keys()))
        state["services"][service] = "failed"
        state["metrics"]["failures"] += 1
        log_incident(state, service, "random_failure")

def auto_heal(state):
    for s in state["services"]:
        if state["services"][s] == "failed":
            if random.random() < 0.3:
                state["services"][s] = "running"
                state["metrics"]["recoveries"] += 1
                log_incident(state, s, "auto_heal")

def apply_action(state, cmd, target):
    reward = 0.0
    done = False

    state["steps"] += 1

    if target not in state["services"]:
        return state, -0.2, False

    current = state["services"][target]

    if cmd == "fail":
        state["services"][target] = "failed"
        state["metrics"]["failures"] += 1
        reward -= 0.3

    elif cmd == "restart":
        if current == "failed":
            reward += 0.7
        elif current == "running":
            reward -= 0.1
        else:
            reward += 0.2

        state["services"][target] = "running"
        state["metrics"]["recoveries"] += 1

    elif cmd == "stop":
        state["services"][target] = "stopped"
        reward -= 0.25

    log_incident(state, target, cmd)

    # stochastic dynamics
    inject_random_failure(state)
    auto_heal(state)

    # goal condition
    if all(s == "running" for s in state["services"].values()):
        reward += 0.5
        done = True

    # step limit
    if state["steps"] >= MAX_STEPS:
        reward -= 0.2
        done = True

    return state, round(reward, 2), done
