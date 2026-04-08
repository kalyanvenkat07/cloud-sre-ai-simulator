import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cloud SRE AI Dashboard", layout="wide")

st.title("🚀 Cloud SRE AI Dashboard")

# ---------------- API ----------------
def get_state():
    try:
        return requests.get(f"{BASE_URL}/state").json()
    except:
        return None

def run(cmd, target):
    try:
        return requests.post(f"{BASE_URL}/step", json={"command": cmd, "target": target}).json()
    except:
        return {"error": "API error"}

def reset():
    requests.post(f"{BASE_URL}/reset")

state = get_state()

if not state:
    st.error("❌ Backend not reachable")
    st.stop()

# ---------------- METRICS ----------------
st.header("📊 Metrics")

col1, col2 = st.columns(2)
col1.metric("Failures", state["metrics"]["failures"])
col2.metric("Recoveries", state["metrics"]["recoveries"])

st.subheader("📈 Trend")
st.line_chart({
    "Failures": [state["metrics"]["failures"]],
    "Recoveries": [state["metrics"]["recoveries"]]
})

# ---------------- SERVICES ----------------
st.header("🖥️ Services")

for s, status in state["services"].items():
    if status == "running":
        st.success(f"{s} Running")
    elif status == "failed":
        st.error(f"{s} Failed")
    else:
        st.warning(f"{s} Stopped")

# ---------------- ACTION ----------------
st.header("⚙️ Control Panel")

cmd = st.selectbox("Command", ["fail", "restart", "stop"])
target = st.selectbox("Service", ["web", "db", "cache"])

if st.button("Execute"):
    res = run(cmd, target)

    if "error" in res:
        st.error(res["error"])
    else:
        st.success("Command executed")

        st.subheader("🤖 AI Analysis")
        st.write(res["ai_response"])

        state = res["state"]

if st.button("Reset System"):
    reset()
    st.success("System reset")
    state = get_state()

# ---------------- INCIDENTS ----------------
st.header("📜 Incident History")

for inc in reversed(state["incidents"]):
    auto = "✅ Yes" if inc["auto_healed"] else "❌ No"

    st.markdown(f"""
**🕒 {inc['time']} | {inc['service'].upper()}**

- ⚙️ Action: {inc['action']}
- 🚨 Severity: {inc['severity']}
- 📉 Impact: {inc['impact']}
- 🔍 Root Cause: {inc['root_cause']}
- 🤖 Auto-Healed: {auto}

---
""")
