---
title: Cloud SRE AI Simulator
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🚀 Cloud SRE AI Simulator

An **AI-powered Site Reliability Engineering (SRE) Simulator** that models real-world cloud failures and provides **intelligent recovery suggestions** using LLMs.

---

## 🌟 Overview

Modern cloud systems require fast and accurate incident response.  
This project simulates cloud failures and enhances decision-making using AI.

👉 Instead of just detecting issues, it **suggests what to do next**.

---

## 🔥 Key Features

### 🖥️ SRE Simulation
- Simulate failures (`fail`)
- Restart services (`restart`)
- Stop services (`stop`)
- Multi-service system (web, db, cache)

### 🤖 AI Assistant
- Suggests recovery actions
- Uses OpenAI-compatible API
- Structured inference flow (START → STEP → END)

### 📊 Metrics Tracking
- Failure count
- Recovery count
- Incident logs

### 🎨 Interactive Dashboard
- Built with Streamlit
- Real-time system state
- One-click actions

---

## 🧠 Architecture
Streamlit UI
↓
FastAPI Backend
↓
Inference Engine (inference.py)
↓
LLM (OpenAI / Hugging Face)


---

## 📡 API Endpoints

| Endpoint | Method | Description |
|--------|--------|------------|
| `/state` | GET | Get system state |
| `/step` | POST | Execute command |
| `/reset` | POST | Reset system |

---

## ⚙️ Environment Variables

- `API_BASE_URL` → AI API URL  
- `MODEL_NAME` → Model name  
- `HF_TOKEN` → Optional token  

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --port 8000

Open:

http://localhost:8000/docs
🧪 Demo Flow
1.Open dashboard
2.Select:
Command → fail
Service → web
3.Click Execute
Result:
Service fails ❌
Metrics update 📊
AI suggests recovery 🤖
🏆 Why This Project
Combines DevOps + AI
Real-world SRE use case
Interactive demo
Clean architecture
🛠️ Tech Stack
FastAPI
Streamlit
OpenAI / Hugging Face
Docker (HF Spaces)
🎤 Pitch

“This project simulates real cloud failures and uses AI to recommend recovery actions, helping engineers respond faster and smarter.”

## 👨‍💻 Author

**Kalyan Venkat**
