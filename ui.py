import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="SRE Dashboard", layout="wide")

st.title("🚀 Cloud SRE AI Dashboard")

# Fetch state
data = {}
try:
    data = requests.get(f"{BASE_URL}/state").json()
except:
    st.error("Backend not reachable")

# ---------------- METRICS ----------------
st.header("📊 Metrics")

col1, col2 = st.columns(2)

if data:
    failures = data["metrics"]["failures"]
    recoveries = data["metrics"]["recoveries"]

    col1.metric("Failures", failures)
    col2.metric("Recoveries", recoveries)

    # Better trend chart
    st.subheader("📈 Trend")
    st.line_chart({
        "Failures": [failures],
        "Recoveries": [recoveries]
    })

# ---------------- SERVICES ----------------
st.header("🖥️ Services Status")

if data:
    for s, status in data["services"].items():
        if status == "running":
            st.success(f"{s.upper()} ✅ Running")
        elif status == "failed":
            st.error(f"{s.upper()} ❌ Failed")
        else:
            st.warning(f"{s.upper()} ⚠️ Stopped")

# ---------------- ACTION ----------------
st.header("⚙️ Run Command")

cmd = st.selectbox("Command", ["fail", "restart", "stop"])
target = st.selectbox("Service", ["web", "db", "cache"])

if st.button("Execute"):
    res = requests.post(f"{BASE_URL}/step", json={
        "command": cmd,
        "target": target
    }).json()

    # AI output
    st.subheader("🤖 AI Analysis")

    if "severity" in res["ai"]:
        severity = res["ai"]["severity"]

        if severity == "HIGH":
            st.error(f"🚨 Severity: {severity}")
        elif severity == "MEDIUM":
            st.warning(f"⚠️ Severity: {severity}")
        else:
            st.success(f"✅ Severity: {severity}")

    st.write(res["ai"]["suggestion"])

    st.subheader("📊 Updated State")
    st.json(res["state"])

# ---------------- INCIDENT HISTORY ----------------
st.header("📜 Incident History")

if data and "incidents" in data:
    if len(data["incidents"]) == 0:
        st.info("No incidents yet")
    else:
        for incident in reversed(data["incidents"]):
            st.write(f"🕒 {incident['time']} | {incident['action']} → {incident['service']}")

# ---------------- RESET ----------------
if st.button("Reset System"):
    requests.post(f"{BASE_URL}/reset")
    st.warning("System Reset Done")
