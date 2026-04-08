def grade(state):
    score = 0.0

    running = sum(1 for s in state["services"].values() if s == "running")
    score += (running / 3) * 0.4

    recoveries = min(state["metrics"]["recoveries"] / 3, 1.0)
    score += recoveries * 0.3

    failures = min(state["metrics"]["failures"] / 3, 1.0)
    score += (1 - failures) * 0.3

    return round(score, 2)
