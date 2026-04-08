import streamlit as st
import requests
from grader import grade
import pandas as pd

API = "http://localhost:8000"

st.set_page_config(page_title="SRE Simulator", layout="wide")

st.title("🚀 Cloud SRE Simulator Dashboard")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("🔄 Reset System"):
    requests.post(f"{API}/reset")
    st.session_state.history = []

state = requests.get(f"{API}/state").json()

score = grade(state)
running = sum(1 for s in state["services"].values() if s == "running")
health = int((running / 3) * 100)

col1, col2, col3 = st.columns(3)
col1.metric("🧠 Score", score)
col2.metric("🏥 Health", f"{health}%")
col3.metric("⚖️ Recoveries", state["metrics"]["recoveries"])

st.subheader("🖥️ Services")

cols = st.columns(3)
for i, (s, status) in enumerate(state["services"].items()):
    icon = "🟢" if status == "running" else "🔴" if status == "failed" else "🟡"
    cols[i].metric(s.upper(), f"{icon} {status}")

st.subheader("⚙️ Action")

cmd = st.selectbox("Command", ["fail", "restart", "stop"])
target = st.selectbox("Target", ["web", "db", "cache"])

if st.button("Execute"):
    requests.post(f"{API}/step", json={"command": cmd, "target": target})

    new_state = requests.get(f"{API}/state").json()
    st.session_state.history.append({
        "step": len(st.session_state.history) + 1,
        "score": grade(new_state),
        "failures": new_state["metrics"]["failures"],
        "recoveries": new_state["metrics"]["recoveries"]
    })

    st.rerun()

st.subheader("📈 Performance")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df.set_index("step"))
else:
    st.info("No actions yet")

st.subheader("📜 Incidents")

for inc in reversed(state["incidents"][-5:]):
    st.write(inc)
