import streamlit as st
import requests

BASE_URL = "http://localhost:7860"  # Hugging Face auto-handles this

st.set_page_config(page_title="Cloud SRE AI Dashboard", layout="wide")

st.title("🚀 Cloud SRE AI Dashboard")

# ----------------------------
# Fetch State
# ----------------------------
def get_state():
    try:
        res = requests.get(f"{BASE_URL}/state")
        return res.json()
    except:
        return None

# ----------------------------
# Execute Command
# ----------------------------
def run_command(command, target):
    try:
        res = requests.post(
            f"{BASE_URL}/step",
            json={"command": command, "target": target}
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}

# ----------------------------
# Reset System
# ----------------------------
def reset_system():
    try:
        requests.post(f"{BASE_URL}/reset")
    except:
        pass

# ----------------------------
# UI Layout
# ----------------------------
state = get_state()

if not state:
    st.error("❌ Backend not reachable")
    st.stop()

# ----------------------------
# Metrics
# ----------------------------
st.header("📊 Metrics")
col1, col2 = st.columns(2)

col1.metric("Failures", state["metrics"]["failures"])
col2.metric("Recoveries", state["metrics"]["recoveries"])

# ----------------------------
# Services
# ----------------------------
st.header("🖥️ Services")

for service, status in state["services"].items():
    if status == "running":
        st.success(f"{service} Running")
    elif status == "failed":
        st.error(f"{service} Failed")
    else:
        st.warning(f"{service} {status}")

# ----------------------------
# Actions
# ----------------------------
st.header("⚙️ Actions")

command = st.selectbox("Command", ["fail", "restart", "stop"])
target = st.selectbox("Service", ["web", "db", "cache"])

if st.button("Execute"):
    result = run_command(command, target)

    if "error" in result:
        st.error(result["error"])
    else:
        st.success("✅ Command executed")

        # AI response
        if "ai_response" in result:
            st.subheader("🤖 AI Suggestion")
            st.write(result["ai_response"])

        state = result["state"]

# ----------------------------
# Reset Button
# ----------------------------
if st.button("Reset System"):
    reset_system()
    st.success("🔄 System Reset")
    state = get_state()

# ----------------------------
# Incident History (FIXED 🔥)
# ----------------------------
st.header("📜 Incident History")

incidents = state.get("incidents", [])

if not incidents:
    st.info("No incidents yet")

for incident in incidents:
    if isinstance(incident, dict):
        st.write(f"🕒 {incident.get('time')} | {incident.get('action')} → {incident.get('service')}")
    else:
        # fallback (prevents crash)
        st.write(f"🕒 {incident}")
