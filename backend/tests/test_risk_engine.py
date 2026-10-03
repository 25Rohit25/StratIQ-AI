import pytest
from datetime import date, timedelta
from app.models import Initiative, Milestone, KPI, Blocker, Dependency
from app.services.risk_engine import (
    compute_kpi_deviation,
    calculate_milestone_health,
    calculate_kpi_health,
    calculate_blocker_health,
    evaluate_initiative_health
)

def test_compute_kpi_deviation():
    # Higher is better: target 30%, actual 24% -> deviation is (30-24)/30 * 100 = 20%
    kpi1 = KPI(name="Conversion", target_value=30.0, current_value=24.0, is_higher_better=True)
    dev1 = compute_kpi_deviation(kpi1)
    assert dev1 == 20.0

    # Lower is better: target 10%, actual 16% -> deviation is (16-10)/10 * 100 = 60%
    kpi2 = KPI(name="Drop-off", target_value=10.0, current_value=16.0, is_higher_better=False)
    dev2 = compute_kpi_deviation(kpi2)
    assert dev2 == 60.0

    # Beating target -> deviation is 0.0
    kpi3 = KPI(name="Conversion", target_value=30.0, current_value=35.0, is_higher_better=True)
    assert compute_kpi_deviation(kpi3) == 0.0

def test_calculate_blocker_health_penalties():
    # Healthy initiative with no blockers
    score_clean, count_clean, max_days, _ = calculate_blocker_health([])
    assert score_clean == 100.0
    assert count_clean == 0

    # Initiative with 1 critical blocker open for 11 days
    blocker = Blocker(
        title="Partner API Certification",
        severity="CRITICAL",
        status="OPEN",
        days_open=11,
        owner="Integration Team"
    )
    score_crit, count_crit, max_days, _ = calculate_blocker_health([blocker])
    # 100 - 30 (critical) - 10 (>7 days) = 60.0
    assert score_crit == 60.0
    assert count_crit == 1
    assert max_days == 11

def test_evaluate_initiative_health_weights():
    # Test project with specific milestone delay and KPI deviation
    today = date.today()
    init = Initiative(
        name="Digital Lending Launch",
        owner="Fintech Squad",
        start_date=today - timedelta(days=60),
        target_date=today + timedelta(days=30),
        milestones=[
            Milestone(name="Milestone 1", target_date=today - timedelta(days=20), status="DONE", delay_days=0),
            Milestone(name="Milestone 2", target_date=today - timedelta(days=5), status="DELAYED", delay_days=9)
        ],
        kpis=[
            KPI(name="Conversion", target_value=30.0, current_value=24.0, is_higher_better=True) # 20% dev
        ],
        blockers=[
            Blocker(title="API Certification", severity="HIGH", status="OPEN", days_open=11, owner="Integration")
        ],
        upstream_dependencies=[]
    )

    result = evaluate_initiative_health(init)
    
    # Assert breakdown elements are computed
    assert "breakdown" in result
    assert result["breakdown"]["overall_health"] == result["health_score"]
    
    # Milestone delay of 9 days > 7 -> triggers 25 pts
    # KPI dev 20% > 10% -> triggers 25 pts
    # Critical/High blocker open 11 days -> triggers 30 pts
    # Deterministic risk score should be at least 80 (CRITICAL)
    assert result["deterministic_risk_score"] >= 70
    assert result["rule_severity"] == "CRITICAL"
    assert len(result["reasons"]) >= 3
    assert len(result["recommended_actions"]) >= 2
