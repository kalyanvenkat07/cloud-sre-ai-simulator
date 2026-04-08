---
title: Cloud SRE AI Simulator
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
tags:
  - openenv
  - sre
  - ai
  - simulation
---
# 🚀 Cloud SRE AI Simulator

## 💡 Overview

The **Cloud SRE AI Simulator** is a real-world environment designed to simulate **Site Reliability Engineering (SRE)** workflows such as service failures, recovery actions, and system stabilization.

It enables **AI agents, developers, and students** to practice incident response, evaluate decision-making strategies, and train intelligent systems in a controlled environment.

---

## 🌍 Real-World Relevance

This simulator mimics real DevOps/SRE scenarios:

| Simulator Action | Real-World Equivalent      |
| ---------------- | -------------------------- |
| `fail`           | Service crash/outage       |
| `restart`        | Pod/container restart      |
| `stop`           | Manual shutdown            |
| auto-heal        | Self-healing systems       |
| incidents        | Monitoring/logging systems |

---

## ⚙️ Features

* 🔥 Real-time failure simulation
* 🤖 Auto-healing system behavior
* 📊 Live scoring dashboard
* 📈 Performance tracking (charts)
* 🧠 AI-friendly environment (OpenEnv ready)
* 🖥️ Interactive UI (Streamlit)
* ⚡ FastAPI backend

---

## 🧠 OpenEnv Compliance

* ✅ Typed Action & Observation models
* ✅ `step()`, `reset()`, `state()` APIs
* ✅ Reward shaping (dense signals)
* ✅ Multi-step environment
* ✅ Deterministic + stochastic behavior

---

## 🎯 Action Space

```json
{
  "command": "fail | restart | stop",
  "target": "web | db | cache"
}
```

---

## 👁️ Observation Space

```json
{
  "services": {
    "web": "running | failed | stopped",
    "db": "running | failed | stopped",
    "cache": "running | failed | stopped"
  },
  "incidents": [],
  "metrics": {
    "failures": 0,
    "recoveries": 0
  },
  "steps": 0
}
```

---

## 🎯 Reward System

| Action                | Reward |
| --------------------- | ------ |
| Correct recovery      | +0.7   |
| Full system stability | +0.5   |
| Useful action         | +0.2   |
| Failure introduced    | -0.3   |
| Stop service          | -0.25  |
| Redundant action      | -0.1   |
| Max steps reached     | -0.2   |

👉 Encourages **efficient, intelligent recovery strategies**

---

## 🔁 Episode Design

* Max steps: **10**
* Episode ends when:

  * All services are running ✅
  * Step limit reached ❌

---

## 📊 Scoring System

Score range: **0.0 → 1.0**

Based on:

* System health
* Recovery efficiency
* Failure minimization

---

## 🖥️ Dashboard

The Streamlit UI provides:

* 🧠 Agent score
* 🏥 System health %
* 📈 Performance graphs
* 📜 Incident history
* ⚙️ Action controls

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --port 8000
streamlit run dashboard.py
```

---

## 🐳 Docker Deployment

```bash
docker build -t sre-ai .
docker run -p 7860:7860 sre-ai
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description       |
| ------ | -------- | ----------------- |
| GET    | /state   | Current state     |
| POST   | /reset   | Reset environment |
| POST   | /step    | Execute action    |

---

## 📈 Baseline

```bash
python baseline.py
```

Expected score:

```
~1.5 – 3.0
```

---

## 🧪 Use Cases

* Reinforcement Learning environments
* AI agent evaluation
* DevOps/SRE training
* Educational simulations

---

## 🏆 Highlights

* Real-world SRE simulation (not a toy problem)
* Dynamic failure + recovery system
* AI-ready environment design
* Interactive UI + backend integration
* Fully containerized & reproducible

---

## 👨‍💻 Author

**Kalyan Venkat**

---

## 🚀 Future Improvements

* Multi-service dependency modeling
* Alert prioritization system
* Autonomous AI agent integration
* Advanced monitoring dashboards

---

⭐ If you like this project, consider giving it a star!
