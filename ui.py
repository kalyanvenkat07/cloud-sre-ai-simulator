import streamlit as st
import requests

# ----------------------------
# Backend URL (FastAPI on 8000)
# ----------------------------
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cloud SRE AI Dashboard", layout="wide")

st.title("🚀 Cloud SRE AI Dashboard")

# ----------------------------
# API FUNCTIONS
# ----------------------------
def get_state():
    try:
        res = requests.get(f"{BASE_URL}/state", timeout=5)
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None


def step(command, target):
    try:
        res = requests.post(
            f"{BASE_URL}/step",
            json={"command": command, "target": target},
            timeout=10
        )
        return res.json()
    except:
        return None


def reset():
    try:
        requests.post(f"{BASE_URL}/reset", timeout=5)
    except:
        pass


# ----------------------------
# LOAD STATE
# ----------------------------
state = get_state()

if not state:
    st.error("❌ Backend not reachable")
    st.stop()

# ----------------------------
# METRICS
# ----------------------------
st.header("📊 Metrics")

col1, col2 = st.columns(2)
col1.metric("Failures", state["metrics"]["failures"])
col2.metric("Recoveries", state["metrics"]["recoveries"])

# Simple trend
st.subheader("📈 System Trend")
st.line_chart({
    "Failures": [state["metrics"]["failures"]],
    "Recoveries": [state["metrics"]["recoveries"]]
})

# ----------------------------
# SERVICES
# ----------------------------
st.header("🖥️ Services")

for service, status in state["services"].items():
    if status == "running":
        st.success(f"{service} Running")
    elif status == "failed":
        st.error(f"{service} Failed")
    else:
        st.warning(f"{service} Stopped")

# ----------------------------
# ACTIONS
# ----------------------------
st.header("⚙️ Control Panel")

command = st.selectbox("Command", ["fail", "restart", "stop"])
target = st.selectbox("Service", ["web", "db", "cache"])

if st.button("Execute"):
    new_state = step(command, target)

    if not new_state:
        st.error("❌ Step failed")
    else:
        st.success("✅ Command executed")

        # Simple AI-like message
        if command == "fail":
            st.warning("🚨 Failure detected → Auto-healing triggered")
        elif command == "restart":
            st.info("🔁 Service restarted successfully")
        elif command == "stop":
            st.warning("⛔ Service stopped")

        state = new_state

# ----------------------------
# RESET
# ----------------------------
if st.button("🔄 Reset System"):
    reset()
    st.success("System reset successful")
    state = get_state()

# ----------------------------
# INCIDENT HISTORY
# ----------------------------
st.header("📜 Incident History")

incidents = state.get("incidents", [])

if not incidents:
    st.info("No incidents yet")

for inc in reversed(incidents):
    auto = "✅ Yes" if inc.get("auto_healed") else "❌ No"

    st.markdown(f"""
**🕒 {inc.get('time')} | {inc.get('service').upper()}**

- ⚙️ Action: {inc.get('action')}
- 🚨 Severity: {inc.get('severity')}
- 📉 Impact: {inc.get('impact')}
- 🔍 Root Cause: {inc.get('root_cause')}
- 🤖 Auto-Healed: {auto}

---
""")
