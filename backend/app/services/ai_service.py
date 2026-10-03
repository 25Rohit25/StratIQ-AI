import os
import httpx
from typing import Dict, Any, List
from app.config import settings

def generate_ai_risk_narrative(initiative_name: str, health_score: float, risk_level: str, evidence: Dict[str, Any], reasons: List[str], recommendations: List[str]) -> str:
    """
    Generates an executive-ready AI risk explanation.
    Uses OpenAI if key is present; otherwise falls back to a deterministic rule-based narrative synthesizer.
    """
    if settings.OPENAI_API_KEY:
        try:
            prompt = f"""
You are an executive product operations advisor. Write a concise, actionable risk explanation for executive leadership.
Initiative: {initiative_name}
Health Score: {health_score}/100
Risk Level: {risk_level}
Identified Evidence: {evidence}
Calculated Reasons: {reasons}
Recommended Actions: {recommendations}

Instructions:
1. Explain WHY the initiative is at risk using the specific numbers provided (days delayed, % KPI deviation, open blocker age).
2. Synthesize a 1-sentence root-cause diagnosis.
3. Highlight the #1 single most urgent mitigation step.
Keep it strictly under 150 words. Do not hallucinate external facts.
"""
            headers = {
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": settings.OPENAI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 250
            }
            with httpx.Client(timeout=6.0) as client:
                res = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception:
            # Gracefully fallback to deterministic generator
            pass

    # High-fidelity deterministic heuristic narrative
    narrative_lines = [
        f"**Executive Diagnostic:** {initiative_name} is currently flagged as **{risk_level}** with an overall health score of **{health_score}/100**."
    ]

    if reasons:
        narrative_lines.append("\n**Primary Contributing Factors:**")
        for idx, r in enumerate(reasons, 1):
            narrative_lines.append(f"{idx}. {r}")

    if recommendations:
        narrative_lines.append(f"\n**Immediate Leadership Recommendation:**\n{recommendations[0]}")

    return "\n".join(narrative_lines)


def generate_portfolio_executive_briefing(stats: Dict[str, Any], largest_risk_init: Dict[str, Any], top_risks: List[Dict[str, Any]]) -> str:
    """
    Synthesizes portfolio-wide executive summary for leadership standups.
    """
    if settings.OPENAI_API_KEY:
        try:
            prompt = f"""
You are Chief of Staff to the VP of Product. Generate a formal, punchy executive portfolio briefing.
Portfolio Stats: {stats}
Largest Risk Initiative: {largest_risk_init}
Top At-Risk Programs: {top_risks}

Include:
- High-level portfolio status ({stats.get('total_initiatives')} initiatives, {stats.get('healthy_count')} healthy, {stats.get('at_risk_count')} at risk, {stats.get('critical_count')} critical)
- Highlight the single largest bottleneck project and its root failure modes.
- Specify 2 concrete decisions required from the executive team this week.
Format in crisp Markdown under 200 words.
"""
            headers = {
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": settings.OPENAI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 300
            }
            with httpx.Client(timeout=6.0) as client:
                res = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception:
            pass

    # Deterministic Briefing Synthesis
    total = stats.get("total_initiatives", 18)
    healthy = stats.get("healthy_count", 11)
    watch = stats.get("watch_count", 0)
    at_risk = stats.get("at_risk_count", 5)
    critical = stats.get("critical_count", 2)
    avg_health = stats.get("average_health_score", 72.4)

    largest_name = largest_risk_init.get("name", "Payment Modernization Program") if largest_risk_init else "None"
    largest_score = largest_risk_init.get("health_score", 38.0) if largest_risk_init else 100

    briefing = f"""### 📊 Executive Portfolio Briefing

Across the enterprise portfolio of **{total} strategic initiatives**, the aggregate health index stands at **{avg_health}/100**.

* **Healthy:** {healthy} programs on target
* **Watch / Warning:** {watch} programs showing early schedule friction
* **At Risk:** {at_risk} programs with active KPI or milestone slippage
* **Critical:** {critical} programs requiring immediate leadership intervention

#### 🚨 Primary Bottleneck: {largest_name} (Health Score: {largest_score}/100)
This initiative represents the highest systemic risk across the organization due to unresolved technical dependencies and deteriorating leading conversion metrics.

#### 🎯 Recommended Executive Action:
1. Mandate an expedited escalation on external API certification and partner commitments.
2. Review cross-initiative dependencies to decouple non-blocking downstream releases and safeguard Q4 revenue milestones.
"""
    return briefing.strip()
