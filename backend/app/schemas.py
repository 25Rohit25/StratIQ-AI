from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import date, datetime

# --- Milestone Schemas ---
class MilestoneBase(BaseModel):
    name: str
    target_date: date
    actual_date: Optional[date] = None
    status: str = "PENDING"
    delay_days: int = 0
    order_index: int = 0

class MilestoneCreate(MilestoneBase):
    pass

class MilestoneOut(MilestoneBase):
    id: int
    initiative_id: int
    class Config:
        from_attributes = True

# --- KPI Schemas ---
class KPIBase(BaseModel):
    name: str
    target_value: float
    current_value: float
    unit: str = "%"
    trend: str = "FLAT"
    is_higher_better: bool = True
    history: Optional[List[float]] = []

class KPICreate(KPIBase):
    pass

class KPIOut(KPIBase):
    id: int
    initiative_id: int
    deviation_pct: Optional[float] = 0.0
    status: Optional[str] = "ON_TARGET"
    class Config:
        from_attributes = True

# --- Blocker Schemas ---
class BlockerBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str = "MEDIUM" # LOW, MEDIUM, HIGH, CRITICAL
    owner: str
    status: str = "OPEN"     # OPEN, IN_PROGRESS, RESOLVED
    days_open: int = 0

class BlockerCreate(BlockerBase):
    pass

class BlockerOut(BlockerBase):
    id: int
    initiative_id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# --- Dependency Schemas ---
class DependencyBase(BaseModel):
    source_initiative_id: int
    target_initiative_id: int
    dependency_type: str = "PREREQUISITE"
    status: str = "ACTIVE"
    impact_severity: str = "HIGH"

class DependencyCreate(DependencyBase):
    pass

class DependencyOut(DependencyBase):
    id: int
    source_initiative_name: Optional[str] = None
    target_initiative_name: Optional[str] = None
    source_risk_level: Optional[str] = None
    class Config:
        from_attributes = True

# --- Stakeholder Schemas ---
class StakeholderBase(BaseModel):
    name: str
    email: str
    team: str
    role: str

class StakeholderCreate(StakeholderBase):
    pass

class StakeholderOut(StakeholderBase):
    id: int
    initiative_id: int
    class Config:
        from_attributes = True

# --- Risk & Diagnostics Schemas ---
class RiskBase(BaseModel):
    risk_type: str
    severity: str
    score: float
    reason: str
    recommended_action: str

class RiskOut(RiskBase):
    id: int
    initiative_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class HealthBreakdown(BaseModel):
    milestone_health: float
    kpi_health: float
    blocker_health: float
    dependency_health: float
    timeline_health: float
    overall_health: float

class RiskDiagnostic(BaseModel):
    initiative_id: int
    initiative_name: str
    health_score: float
    risk_level: str
    deterministic_risk_score: float
    rule_severity: str
    health_breakdown: HealthBreakdown
    reasons: List[str]
    evidence: Dict[str, Any]
    recommended_actions: List[str]
    ai_narrative: Optional[str] = None

# --- Initiative Schemas ---
class InitiativeBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner: str
    status: str = "ON_TRACK"
    category: str = "Core Product"
    priority: str = "HIGH"
    start_date: date
    target_date: date
    budget: Optional[float] = 0.0

class InitiativeCreate(InitiativeBase):
    pass

class InitiativeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    target_date: Optional[date] = None
    budget: Optional[float] = None

class InitiativeSummary(InitiativeBase):
    id: int
    health_score: float
    risk_level: str
    open_blockers_count: int = 0
    kpi_count: int = 0
    milestone_count: int = 0
    upstream_count: int = 0
    downstream_count: int = 0
    class Config:
        from_attributes = True

class InitiativeDetail(InitiativeSummary):
    milestones: List[MilestoneOut] = []
    kpis: List[KPIOut] = []
    blockers: List[BlockerOut] = []
    stakeholders: List[StakeholderOut] = []
    risks: List[RiskOut] = []
    upstream_dependencies: List[DependencyOut] = []
    downstream_dependencies: List[DependencyOut] = []
    diagnostic: Optional[RiskDiagnostic] = None
    class Config:
        from_attributes = True

# --- Portfolio & Executive Summary Schemas ---
class PortfolioHealthStats(BaseModel):
    total_initiatives: int
    healthy_count: int      # 80-100
    watch_count: int        # 60-79
    at_risk_count: int      # 40-59
    critical_count: int     # 0-39
    completed_count: int
    average_health_score: float
    total_open_blockers: int
    critical_blockers_count: int
    top_risks: List[Dict[str, Any]]

class ExecutiveSummaryResponse(BaseModel):
    timestamp: datetime
    portfolio_stats: PortfolioHealthStats
    largest_risk_initiative: Optional[Dict[str, Any]]
    primary_failure_causes: List[str]
    executive_recommendations: List[str]
    briefing_narrative: str

# --- Change Impact Analysis Schemas ---
class ImpactAnalysisRequest(BaseModel):
    initiative_id: int
    simulated_delay_days: int = 14
    reason_for_delay: Optional[str] = "Upstream architectural delay"

class ImpactedInitiative(BaseModel):
    initiative_id: int
    name: str
    owner: str
    original_target_date: date
    new_projected_date: date
    direct_or_cascading: str # DIRECT, CASCADING_LEVEL_1, CASCADING_LEVEL_2, etc.
    original_risk_level: str
    projected_risk_level: str
    affected_kpis: List[str]
    affected_stakeholders: List[str]

class ImpactAnalysisResponse(BaseModel):
    source_initiative_id: int
    source_initiative_name: str
    simulated_delay_days: int
    total_affected_initiatives: int
    impacted_initiatives: List[ImpactedInitiative]
    critical_path_delayed: bool
    summary: str
    mitigation_recommendations: List[str]
