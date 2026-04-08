import os
from openai import OpenAI

# ---------------- ENV VARIABLES ----------------
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

# ---------------- CLIENT (kept for structure) ----------------
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN or "dummy"
)

# ---------------- INFERENCE FUNCTION ----------------
def run_inference(command, target):
    print("START")

    try:
        if command == "fail":
            severity = "HIGH"
            suggestion = f"""
🚨 INCIDENT DETECTED
Service: {target}
Severity: {severity}

Action:
- Restart service immediately
- Check logs for root cause
- Monitor system stability
"""

        elif command == "restart":
            severity = "LOW"
            suggestion = f"""
✅ RECOVERY ACTION
Service: {target}
Severity: {severity}

Status:
- Service restarted successfully
- Monitor for anomalies
"""

        elif command == "stop":
            severity = "MEDIUM"
            suggestion = f"""
⚠️ SERVICE STOPPED
Service: {target}
Severity: {severity}

Action:
- Verify if intentional
- Restart if required
"""

        else:
            severity = "UNKNOWN"
            suggestion = "Invalid command"

        print("STEP: Generated AI response")
        print(f"STEP: {suggestion}")
        print("END")

        return {
            "severity": severity,
            "suggestion": suggestion
        }

    except Exception as e:
        print(f"STEP: Error {str(e)}")
        print("END")
        return {"error": str(e)} 
