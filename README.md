# StratIQ AI ⚡
### AI-Powered Strategic Initiative & Project Risk Intelligence Platform

> **Turn Operational Signals into Explainable Risks, Root-Cause Diagnostics, and High-Leverage Strategic Interventions.**

---

## 💡 Overview & Problem Statement
Enterprise organizations juggle dozens of strategic programs concurrently (e.g. *Digital Lending Launch*, *Cloud Infrastructure Migration*, *Payment Modernization*, *Market Expansion*). However, mission-critical operational data remains siloed across Jira boards, static spreadsheets, slide presentations, and ad-hoc status meetings.

**Executives struggle to answer:**
- *Which initiatives are genuinely at risk before a deadline slips?*
- *Why are they at risk (metrics, dependencies, or blockers)?*
- *If Project A slips by 14 days, which downstream launches and revenue KPIs break?*
- *What is the highest-ROI leadership action to take today?*

**StratIQ AI** bridges this gap by unifying deterministic quantitative risk engines with AI-driven root-cause explanations and change impact simulations.

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| **📊 Executive Portfolio Command** | Real-time health distribution (Healthy, Watch, At Risk, Critical), priority alerts, and portfolio health index. |
| **🎯 5-Factor Health Scoring Engine** | Transparent, formulaic 0–100 score: 30% Milestones + 25% KPIs + 20% Blockers + 15% Dependencies + 10% Timeline. |
| **🔍 Explainable AI Diagnostics** | Deterministic evidence-backed risk analysis with natural-language executive rationales and actionable mitigations. |
| **📈 KPI & Milestone Tracker** | Target vs Actual tracking, % negative deviation alerts, milestone slippage tracking, and blocker aging analysis. |
| **🕸️ Interactive Dependency Graph** | Visual network of initiatives showing upstream requirements and downstream cascading risk paths. |
| **⚡ What-If Change Impact Simulator** | Simulate schedule delays on any initiative to project downstream cascade delays, affected stakeholders, and endangered KPIs. |
| **📋 AI Executive Briefings** | Instant synthesis of portfolio risks, primary failure modes, and leadership recommendations for C-Suite reviews. |
| **🎓 Product Management Studio** | Interactive RICE Prioritization Calculator, PRD Explorer, and Mock User Discovery research insights. |

---

## 🏛️ System Architecture

```
                       ┌──────────────────────────────┐
                       │   React + TypeScript + Vite  │
                       │   (Modern Cyber-Dark UI)     │
                       └──────────────┬───────────────┘
                                      │ REST API / JSON
                                      ▼
                       ┌──────────────────────────────┐
                       │       FastAPI (Python)       │
                       └──────┬───────┬────────┬──────┘
                              │       │        │
               ┌──────────────┘       │        └──────────────┐
               ▼                      ▼                       ▼
    ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
    │  Project Service   │ │ Deterministic Risk │ │ AI Explanation &   │
    │  & Seed Generator  │ │ & Health Engine    │ │ Impact Simulator   │
    └──────────┬─────────┘ └──────────┬─────────┘ └──────────┬─────────┘
               │                      │                      │
               ▼                      ▼                      ▼
    ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
    │ SQLite / Postgres  │ │ Multi-factor Risk  │ │ LLM / Heuristic    │
    │ (SQLAlchemy ORM)   │ │ Mathematical Model │ │ Reasoning Engine   │
    └────────────────────┘ └────────────────────┘ └────────────────────┘
```

---

## 🛠️ Tech Stack

* **Frontend:** React 19, TypeScript, Vite, Vanilla CSS Design System (Executive Glassmorphism & Cyber-Dark theme), Lucide Icons.
* **Backend:** Python 3.12, FastAPI, SQLAlchemy, Pydantic v2, Uvicorn.
* **Data & Analytics:** Deterministic Graph Traversals, NumPy/Pandas logic.
* **AI & Intelligence:** Deterministic Evidence Extractor + High-fidelity LLM prompt engine (with built-in offline heuristic fallback).
* **Database:** SQLite (zero-config local default) with instant PostgreSQL compatibility via standard `DATABASE_URL`.

---

## ⚡ Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend API will be running at: `http://localhost:8000`  
Interactive Swagger docs: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend Web App will be running at: `http://localhost:5173`

---

## 📐 Health Score Formula

$$\text{Health Score} = 0.30 \times M + 0.25 \times K + 0.20 \times B + 0.15 \times D + 0.10 \times T$$

* **Milestone Health ($M$):** Schedule adherence and slippage penalty.
* **KPI Health ($K$):** Variance between actual and target KPI metrics.
* **Blocker Health ($B$):** Severity-weighted open blocker count and aging ($>7$ days penalty).
* **Dependency Health ($D$):** Weighted health of upstream prerequisite initiatives.
* **Timeline Health ($T$):** Elapsed calendar duration vs delivered scope.

---

## 👥 Author & Context
Created as a flagship Strategic Product Management & Decision Intelligence portfolio platform demonstrating KPI governance, risk engineering, dependency topologies, and AI-assisted leadership synthesis.
