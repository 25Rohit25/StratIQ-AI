# Product Requirements Document (PRD)
## StratIQ AI: Strategic Initiative & Project Risk Intelligence Platform

---

### 1. Document Overview
* **Product Name:** StratIQ AI
* **Version:** 1.0.0
* **Target Audience:** Product Managers, Program Managers, PMO Leaders, Operations Directors, C-Suite / VP Executives
* **Author / PM Lead:** Product Intern / Strategic Planning Lead

---

### 2. Problem Statement
Modern enterprises run dozens of strategic initiatives simultaneously (e.g., *Digital Lending Launch*, *Payment API Modernization*, *Cloud Infrastructure Migration*, *Compliance & Open Banking*). However, operational project signals are fragmented across spreadsheets, Jira boards, slide decks, and disparate status emails.

**Key Executive Pain Points:**
1. **Lack of Early Warning:** Initiatives are flagged as "Red" only after missing major deadlines, not when leading indicators (KPI slippage, API delays) first appear.
2. **Hidden Cascading Dependencies:** When a foundational initiative slips (e.g., Compliance Approval), down-stream launches (Mobile Checkout, Merchant Subscriptions) face invisible ripple effects.
3. **Black-box Status Reporting:** Traditional "RAG" (Red/Amber/Green) statuses rely on subjective human self-reporting rather than deterministic, auditable evidence.
4. **Action Paralysis:** Standard dashboards report that a project is late without diagnosing *why* or recommending high-leverage interventions.

---

### 3. Product Vision & Value Proposition
StratIQ AI converts raw operational signals into **Explainable Risk Intelligence & Decision Support**:
$$\text{Signals} \longrightarrow \text{Risks} \longrightarrow \text{Evidence Explanations} \longrightarrow \text{Recommended Actions}$$

Rather than passive dashboards, StratIQ provides:
- **0–100 Weighted Objective Health Scoring**
- **Deterministic Risk Rules paired with Natural Language Explanations**
- **Interactive Upstream/Downstream Dependency Cascades**
- **What-If Change Impact Simulation** (e.g., "What happens to the portfolio if Payment API slips by 14 days?")
- **Automated AI Executive Briefings**

---

### 4. User Personas & Core Journeys

| Persona | Role | Key Jobs to be Done | Core Features Used |
| :--- | :--- | :--- | :--- |
| **Priya (Product Manager)** | Owns single initiative execution | Monitor KPIs, spot milestone slippage, log and unblock technical dependencies. | Milestone Tracker, KPI Monitor, Blocker Manager |
| **Marcus (Program Manager)** | Coordinates cross-initiative portfolio | Map cross-team dependencies, spot bottleneck projects, prevent launch collisions. | Dependency Graph, What-If Impact Simulator |
| **Elena (VP / Executive)** | Strategic budget & resource allocator | Identify top at-risk investments, understand root causes in seconds, approve interventions. | Executive Portfolio Dashboard, AI Briefings |
| **Dave (Operations Lead)** | Cross-functional delivery execution | Track resolution time of high-severity blockers, assign clear ownership. | Blocker Tracker, SLA Alerts |

---

### 5. Core Feature Specifications & Acceptance Criteria

#### Feature 1: 5-Factor Initiative Health Score Engine
* **Logic:** Computes a transparent, reproducible 0–100 score:
  $$\text{Health Score} = 0.30 \times M + 0.25 \times K + 0.20 \times B + 0.15 \times D + 0.10 \times T$$
  * $M$ (Milestone Health): Ratio of completed / on-schedule milestones minus delay penalties.
  * $K$ (KPI Health): Average performance against targets ($100 - \text{average negative deviation}$).
  * $B$ (Blocker Health): Penalties for open blockers weighted by severity (Critical: -30, High: -15, Medium: -8) and age (>7 days open).
  * $D$ (Dependency Health): Health score of upstream initiatives blocking this project.
  * $T$ (Timeline Health): Days remaining vs percentage of scope completed.
* **Risk Categorization:**
  * **80 – 100:** Healthy (Green)
  * **60 – 79:** Watch (Amber)
  * **40 – 59:** At Risk (Orange)
  * **0 – 39:** Critical (Red)

#### Feature 2: Explainable Risk Diagnostic Engine
* **User Story:** *As an Executive, I want to know exactly WHY an initiative is at risk with quantitative evidence, so I can trust the assessment.*
* **Acceptance Criteria:**
  1. Risk score is computed deterministically first (Milestone delay $>7\text{d}$, KPI deviation $>10\%$, Critical blockers $>0$, Unresolved dependency).
  2. The system outputs bulleted root causes referencing specific metrics (e.g., *"Conversion KPI is 14% below target"*).
  3. Provides concrete, prioritized mitigation recommendations (e.g., *"Escalate partner API resolution before committing ad spend"*).

#### Feature 3: Interactive Dependency & Cascading Risk Graph
* **User Story:** *As a Program Manager, I want to visualize all upstream and downstream initiative dependencies, so I can predict how a single delay impacts the entire product suite.*
* **Acceptance Criteria:**
  1. Interactive node graph displaying initiatives and directional dependency arrows.
  2. Visual color-coding by risk status.
  3. Clicking any initiative highlights its upstream dependencies (what it needs) and downstream dependencies (what it blocks).
  4. Real-time detection of dependency cycles.

#### Feature 4: What-If Change Impact Simulator
* **User Story:** *As a PM or Director, I want to simulate an $N$-day delay on an initiative to see which dependent projects, launch dates, KPIs, and stakeholders are affected.*
* **Acceptance Criteria:**
  1. User selects any initiative and specifies hypothetical delay (e.g., $+14$ days).
  2. Traverses downstream dependency tree.
  3. Displays list of impacted initiatives, new projected completion dates, affected stakeholders, and revenue/conversion KPIs at risk.
  4. Generates mitigation checklist.

#### Feature 5: AI Executive Summary & Portfolio Briefing
* **User Story:** *As a VP of Product, I want an on-demand executive briefing summarizing portfolio health, primary risk drivers, and recommended decisions for leadership standups.*
* **Acceptance Criteria:**
  1. Aggregates portfolio metrics across all tracked initiatives.
  2. Identifies the #1 single largest risk project and common failure modes.
  3. Formats an executive-ready action brief copyable to Slack or email.

---

### 6. Product Prioritization: RICE Framework

| Feature | Reach (1–10) | Impact (1–10) | Confidence (1–10) | Effort (1–10) | RICE Score $\left(\frac{R \times I \times C}{E}\right)$ | Priority |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Risk Dashboard & Health Engine** | 9 | 9 | 9 | 4 | **182.25** | P0 |
| **Explainable AI Root-Cause Diagnostic** | 8 | 9 | 9 | 4 | **162.00** | P0 |
| **KPI Deviation & Trend Monitoring** | 8 | 8 | 8 | 3 | **170.67** | P0 |
| **Change Impact Simulator (What-If)** | 7 | 9 | 8 | 5 | **100.80** | P1 |
| **Interactive Dependency Network Graph** | 6 | 9 | 7 | 5 | **75.60** | P1 |
| **Automated Executive Briefing Generator**| 7 | 8 | 8 | 4 | **112.00** | P1 |
| **Slack / Jira Webhook Integration** | 5 | 6 | 7 | 6 | **35.00** | P2 |

---

### 7. Product Discovery & Mock User Research Findings
Conducted structured interviews with 8 cross-functional leads (4 Product Managers, 2 Engineering Managers, 2 Program Directors):

* **Insight 1 (Fragmented Truth):** 100% of participants reported maintaining separate "executive slides" distinct from Jira/Linear because technical boards are too noisy for leadership.
* **Insight 2 (Unclear Blocker Ownership):** 75% stated blockers often linger $>10$ days because cross-team dependencies lack designated single-threaded owners.
* **Insight 3 (Late Dependency Surprises):** 62% experienced launch delays due to unannounced delays in upstream shared services (Auth, Payment Gateway, Compliance).
* **PM Takeaway:** StratIQ AI directly addresses these 3 core pain points by automating executive synthesis, tracking blocker aging, and visualizing dependency cascades.

---

### 8. Product Success Metrics (KPIs)
* **WAU (Weekly Active Users):** Frequency of PMs and leaders checking portfolio health.
* **Risk Review Rate:** $\frac{\text{Flagged Risks Acknowledged / Reviewed by Owners}}{\text{Total Flagged Risks}} \ge 85\%$.
* **Recommendation Acceptance Rate:** $\frac{\text{Suggested Actions Adopted}}{\text{Suggested Actions Displayed}} \ge 40\%$.
* **Time to Detect Risk (TTDR):** Target $\le 24$ hours from leading indicator shift (vs $\sim 14$ days in traditional monthly reviews).
* **Blocker Resolution SLA:** Reduction of average blocker open duration from 11.4 days to $<4.5$ days.
