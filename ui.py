import streamlit as st
import requests

# ----------------------------
# IMPORTANT: Backend URL (HF Docker Compatible)
# ----------------------------
BASE_URL = "http://127.0.0.1:7860"

st.set_page_config(page_title="Cloud SRE AI Dashboard", layout="wide")

st.title("🚀 Cloud SRE AI Dashboard")

# ----------------------------
# Helper Functions
# ----------------------------
def get_state():
    try:
        res = requests.get(f"{BASE_URL}/state", timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"❌ Backend not reachable: {e}")
        return None


def run_command(command, target):
    try:
        res = requests.post(
            f"{BASE_URL}/step",
            json={"command": command, "target": target},
            timeout=10
        )
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def reset_system():
    try:
        requests.post(f"{BASE_URL}/reset", timeout=5)
    except Exception as e:
        st.error(f"Reset failed: {e}")


# ----------------------------
# Load State
# ----------------------------
state = get_state()

if state is None:
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

        # AI Output
        if "ai_response" in result:
            st.subheader("🤖 AI Suggestion")
            st.write(result["ai_response"])

        state = result["state"]

# ----------------------------
# Reset Button
# ----------------------------
if st.button("🔄 Reset System"):
    reset_system()
    st.success("System reset successfully")
    state = get_state()

# ----------------------------
# Incident History (SAFE + REQUIRED)
# ----------------------------
st.header("📜 Incident History")

incidents = state.get("incidents", [])

if not incidents:
    st.info("No incidents yet")

for incident in incidents:
    if isinstance(incident, dict):
        st.write(
            f"🕒 {incident.get('time', '')} | "
            f"{incident.get('action', '')} → {incident.get('service', '')}"
        )
    else:
        # fallback safety (prevents crash)
        st.write(f"🕒 {incident}")
