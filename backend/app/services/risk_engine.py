from datetime import date, datetime
from typing import List, Dict, Any, Tuple
from app.models import Initiative, Milestone, KPI, Blocker, Dependency

def compute_kpi_deviation(kpi: KPI) -> float:
    """Computes percentage deviation against target."""
    if kpi.target_value == 0:
        return 0.0
    if kpi.is_higher_better:
        if kpi.current_value < kpi.target_value:
            return round(((kpi.target_value - kpi.current_value) / abs(kpi.target_value)) * 100, 1)
        return 0.0
    else:
        if kpi.current_value > kpi.target_value:
            return round(((kpi.current_value - kpi.target_value) / abs(kpi.target_value)) * 100, 1)
        return 0.0

def calculate_milestone_health(milestones: List[Milestone]) -> Tuple[float, int, int]:
    """Calculates milestone health component (0 - 100)."""
    if not milestones:
        return 85.0, 0, 0
    
    total = len(milestones)
    completed = sum(1 for m in milestones if m.status in ["DONE", "COMPLETED"])
    delayed = sum(1 for m in milestones if m.status == "DELAYED" or m.delay_days > 0)
    max_delay = max((m.delay_days for m in milestones), default=0)

    # Base progress score
    base_score = (completed / total) * 100.0
    # Penalty for delays
    delay_penalty = (delayed * 12.0) + (min(max_delay, 30) * 1.5)
    
    # In-progress credit
    in_progress = sum(1 for m in milestones if m.status == "IN_PROGRESS")
    credit = in_progress * 10.0

    score = max(5.0, min(100.0, base_score + credit - delay_penalty))
    return round(score, 1), delayed, max_delay

def calculate_kpi_health(kpis: List[KPI]) -> Tuple[float, List[Dict[str, Any]], float]:
    """Calculates KPI health component (0 - 100)."""
    if not kpis:
        return 85.0, [], 0.0
    
    deviations = []
    total_dev = 0.0
    worst_dev = 0.0

    for kpi in kpis:
        dev = compute_kpi_deviation(kpi)
        deviations.append({
            "name": kpi.name,
            "target": kpi.target_value,
            "actual": kpi.current_value,
            "unit": kpi.unit,
            "deviation_pct": dev,
            "trend": kpi.trend,
            "is_deviating": dev > 0
        })
        total_dev += dev
        if dev > worst_dev:
            worst_dev = dev
    
    avg_dev = total_dev / len(kpis)
    score = max(5.0, min(100.0, 100.0 - (avg_dev * 1.8)))
    return round(score, 1), deviations, worst_dev

def calculate_blocker_health(blockers: List[Blocker]) -> Tuple[float, int, int, List[Blocker]]:
    """Calculates blocker health component (0 - 100)."""
    active_blockers = [b for b in blockers if b.status != "RESOLVED"]
    if not active_blockers:
        return 100.0, 0, 0, []
    
    score = 100.0
    critical_count = 0
    max_days = 0

    for b in active_blockers:
        if b.days_open > max_days:
            max_days = b.days_open
            
        sev = b.severity.upper() if b.severity else "MEDIUM"
        if sev == "CRITICAL":
            critical_count += 1
            score -= 30.0
            if b.days_open > 7:
                score -= 10.0
        elif sev == "HIGH":
            critical_count += 1
            score -= 18.0
            if b.days_open > 7:
                score -= 6.0
        elif sev == "MEDIUM":
            score -= 10.0
            if b.days_open > 10:
                score -= 4.0
        else: # LOW
            score -= 4.0

    return max(0.0, min(100.0, round(score, 1))), len(active_blockers), max_days, active_blockers

def calculate_dependency_health(upstream_deps: List[Dependency]) -> Tuple[float, List[str]]:
    """Calculates dependency health component (0 - 100) based on upstream health."""
    active_deps = [d for d in upstream_deps if d.status == "ACTIVE"]
    if not active_deps:
        return 100.0, []
    
    score = 100.0
    troubled_upstream = []

    for dep in active_deps:
        source = dep.source_initiative
        if source:
            source_risk = source.risk_level.upper() if source.risk_level else "HEALTHY"
            if source_risk == "CRITICAL":
                score -= 35.0
                troubled_upstream.append(f"{source.name} (CRITICAL)")
            elif source_risk == "AT_RISK":
                score -= 22.0
                troubled_upstream.append(f"{source.name} (AT RISK)")
            elif source_risk == "WATCH":
                score -= 10.0
                troubled_upstream.append(f"{source.name} (WATCH)")
    
    return max(10.0, min(100.0, round(score, 1))), troubled_upstream

def calculate_timeline_health(start_date: date, target_date: date, milestone_health: float) -> float:
    """Calculates timeline adherence health (0 - 100)."""
    today = date.today()
    total_days = max(1, (target_date - start_date).days)
    elapsed_days = (today - start_date).days

    if elapsed_days <= 0:
        return 95.0
    if elapsed_days >= total_days:
        # Over target date
        overdue_days = elapsed_days - total_days
        return max(5.0, round(100.0 - (overdue_days * 3.0), 1))
    
    timeline_ratio = elapsed_days / total_days
    # If 70% of time has elapsed but milestone health is poor (<50), penalize
    if timeline_ratio > 0.6 and milestone_health < 50.0:
        return max(20.0, round(milestone_health * 0.8, 1))
    
    return round(max(30.0, min(100.0, 95.0 - (timeline_ratio * 15.0))), 1)

def evaluate_initiative_health(initiative: Initiative) -> Dict[str, Any]:
    """
    Computes overall 5-factor health score:
    Health Score = 30% milestone + 25% KPI + 20% blocker + 15% dependency + 10% timeline
    """
    m_health, delayed_count, max_delay = calculate_milestone_health(initiative.milestones)
    k_health, kpi_devs, worst_kpi_dev = calculate_kpi_health(initiative.kpis)
    b_health, active_blockers, max_blocker_days, blocker_objs = calculate_blocker_health(initiative.blockers)
    d_health, troubled_deps = calculate_dependency_health(initiative.upstream_dependencies)
    
    start_d = initiative.start_date if initiative.start_date else date.today()
    target_d = initiative.target_date if initiative.target_date else date.today()
    t_health = calculate_timeline_health(start_d, target_d, m_health)

    overall = (
        0.30 * m_health +
        0.25 * k_health +
        0.20 * b_health +
        0.15 * d_health +
        0.10 * t_health
    )
    overall_rounded = round(max(0.0, min(100.0, overall)), 1)

    # Determine risk category
    if overall_rounded >= 80.0:
        risk_level = "HEALTHY"
    elif overall_rounded >= 60.0:
        risk_level = "WATCH"
    elif overall_rounded >= 40.0:
        risk_level = "AT_RISK"
    else:
        risk_level = "CRITICAL"

    # Deterministic Rule Engine for Explainable Risks (Section 17)
    deterministic_risk_score = 0
    reasons = []
    recommendations = []

    # Rule 1: Milestone Delay > 7 days
    if max_delay > 7:
        deterministic_risk_score += 25
        reasons.append(f"Milestone delayed by {max_delay} days (exceeds 7-day operational tolerance).")
        recommendations.append("Review milestone critical path and decouple non-essential release requirements.")
    elif delayed_count > 0:
        reasons.append(f"{delayed_count} milestone(s) are running behind schedule.")

    # Rule 2: KPI Deviation > 10%
    deviating_kpis = [k for k in kpi_devs if k["deviation_pct"] > 10.0]
    if deviating_kpis:
        deterministic_risk_score += 25
        kpi_bullets = ", ".join([f"{k['name']} ({k['deviation_pct']}% below target)" for k in deviating_kpis])
        reasons.append(f"Key performance indicators deteriorating: {kpi_bullets}.")
        recommendations.append(f"Reallocate sprint capacity to investigate conversion funnel and retention anomalies.")

    # Rule 3: Critical Blockers > 0
    crit_or_high = [b for b in blocker_objs if b.severity in ["CRITICAL", "HIGH"]]
    if len(crit_or_high) > 0:
        deterministic_risk_score += 30
        longest_blocker = max(crit_or_high, key=lambda x: x.days_open)
        reasons.append(
            f"{len(crit_or_high)} critical/high severity blocker(s) unresolved. "
            f"Blocker '{longest_blocker.title}' has been open for {longest_blocker.days_open} days under {longest_blocker.owner}."
        )
        recommendations.append(
            f"Escalate '{longest_blocker.title}' to executive sponsor and hold single-threaded resolution standup."
        )

    # Rule 4: Unresolved Dependency
    if troubled_deps:
        deterministic_risk_score += 20
        reasons.append(f"High vulnerability to delayed upstream dependencies: {', '.join(troubled_deps)}.")
        recommendations.append("Establish explicit API contracts and fallback mocks with upstream technical leads.")

    # Rule Severity Classification
    if deterministic_risk_score >= 70:
        rule_severity = "CRITICAL"
    elif deterministic_risk_score >= 50:
        rule_severity = "HIGH"
    elif deterministic_risk_score >= 30:
        rule_severity = "MEDIUM"
    else:
        rule_severity = "LOW"

    if not reasons:
        reasons.append("All milestones, KPIs, and dependency contracts are currently tracking within acceptable tolerances.")
    if not recommendations:
        recommendations.append("Maintain existing sprint cadence and monitor leading conversion indicators weekly.")

    return {
        "health_score": overall_rounded,
        "risk_level": risk_level,
        "deterministic_risk_score": deterministic_risk_score,
        "rule_severity": rule_severity,
        "breakdown": {
            "milestone_health": m_health,
            "kpi_health": k_health,
            "blocker_health": b_health,
            "dependency_health": d_health,
            "timeline_health": t_health,
            "overall_health": overall_rounded
        },
        "reasons": reasons,
        "recommended_actions": recommendations,
        "evidence": {
            "delayed_milestones_count": delayed_count,
            "max_milestone_delay_days": max_delay,
            "worst_kpi_deviation_pct": worst_kpi_dev,
            "kpi_deviations": kpi_devs,
            "active_blockers_count": active_blockers,
            "max_blocker_days_open": max_blocker_days,
            "troubled_upstream_dependencies": troubled_deps
        }
    }
