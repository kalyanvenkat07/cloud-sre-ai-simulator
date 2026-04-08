def easy(state):
    return all(s == "running" for s in state["services"].values())

def medium(state):
    return (
        state["metrics"]["recoveries"] >= 2 and
        state["metrics"]["failures"] <= 2
    )

def hard(state):
    return (
        all(s == "running" for s in state["services"].values()) and
        state["metrics"]["recoveries"] >= 3 and
        len(state["incidents"]) >= 3 and
        state["metrics"]["failures"] <= 2
    )
