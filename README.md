---
title: Cloud SRE AI Simulator
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🚀 Cloud SRE AI Simulator  
### AI-Powered Failure Simulation, Intelligent Analysis & Auto-Healing System  

> Simulate cloud failures, analyze incidents, and automatically recover systems using AI-driven logic.

---

## 🔗 Live Demo
👉 **[Open App](https://huggingface.co/spaces/kalyanvenkat-09/cloudsre-env)**

---

## 📸 Demo Preview

### 🟢 Normal System State
![Normal](screenshot1.png)

### 🚨 Failure + Auto-Healing
![Failure](screenshot2.png)

### 📜 Incident Intelligence
![History](screenshot3.png)

---

## 🌟 Overview

This project is a **complete OpenEnv-compatible environment** that simulates real-world cloud infrastructure failures and integrates **AI-style reasoning with auto-healing capabilities**.

It enables:
- Failure simulation  
- Intelligent incident analysis  
- Automatic recovery (self-healing systems)  
- Real-time monitoring  

---

## 🔥 Key Features

### ⚙️ OpenEnv API (Core Requirement)
- `GET /state` → Current system state  
- `POST /step` → Execute actions  
- `POST /reset` → Reset environment  

---

### 🖥️ Cloud Simulation
- Multi-service system (`web`, `db`, `cache`)  
- Simulate failures, restarts, and shutdowns  

---

### 🤖 AI-Driven Analysis
- Severity classification (**HIGH / MEDIUM / LOW**)  
- Root cause detection  
- Impact analysis  
- Actionable recovery recommendations  

---

### 🔁 Auto-Healing System (🔥 Highlight Feature)
- Detects failure events  
- Automatically restores services  
- Updates recovery metrics  
- Mimics real-world self-healing infrastructure  

---

### 📊 Real-Time Dashboard
- Built using Streamlit  
- Live metrics (failures & recoveries)  
- System health visualization  
- Interactive control panel  

---

### 📜 Incident Intelligence
Each incident logs:
- Timestamp  
- Service affected  
- Severity  
- Impact  
- Root cause  
- Auto-healing status  

---

## 🧠 Architecture
Streamlit UI (Port 7860)
↓
FastAPI Backend (Port 8000)
↓
SRE Simulation Engine
↓
AI Logic + Auto-Healing


---

## ⚙️ Tech Stack

- FastAPI (Backend API)  
- Streamlit (Frontend UI)  
- Python  
- Docker (Hugging Face Spaces)  

---

## 📡 API Example

### ▶️ Step Request

```json
{
  "command": "fail",
  "target": "web"
}
✅ Response
{
  "state": {...},
  "ai_response": "...",
  "incident": {...}
}
🧪 Demo Flow
1.Select:
2.Command → fail
Service → web
3.Click Execute
Result:
Service fails ❌
Auto-healing triggers 🔁
Service recovers ✅
Metrics update 📊
AI analysis generated 🤖
🏆 Why This Project Stands Out
Combines DevOps + AI + Simulation
Implements real-world SRE practices
Includes auto-healing (rare in hackathons)
Fully OpenEnv compliant
Clean architecture and UI
🎤 Pitch

“This project simulates real cloud failures and enhances reliability engineering by combining AI-driven analysis with automatic self-healing systems.”

👨‍💻 Author

Kalyan Venkat
