import requests

BASE = "http://localhost:7860"

def run():
    requests.post(f"{BASE}/reset")

    actions = [
        {"command": "fail", "target": "web"},
        {"command": "restart", "target": "web"},
        {"command": "fail", "target": "db"},
        {"command": "restart", "target": "db"},
        {"command": "restart", "target": "cache"},
    ]

    total = 0

    for a in actions:
        r = requests.post(f"{BASE}/step", json=a).json()
        total += r["reward"]["score"]

    print("Baseline Score:", round(total, 2))

if __name__ == "__main__":
    run()
