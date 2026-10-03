from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.database import Base

class Initiative(Base):
    __tablename__ = "initiatives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner = Column(String(255), nullable=False, index=True)
    status = Column(String(50), default="ON_TRACK")  # ON_TRACK, WATCH, AT_RISK, CRITICAL, COMPLETED
    category = Column(String(100), default="Core Product")
    priority = Column(String(50), default="HIGH")     # LOW, MEDIUM, HIGH, CRITICAL
    start_date = Column(Date, default=date.today)
    target_date = Column(Date, nullable=False)
    budget = Column(Float, default=0.0)
    health_score = Column(Float, default=85.0)       # 0 - 100
    risk_level = Column(String(50), default="HEALTHY") # HEALTHY, WATCH, AT_RISK, CRITICAL
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    milestones = relationship("Milestone", back_populates="initiative", cascade="all, delete-orphan", order_by="Milestone.order_index")
    kpis = relationship("KPI", back_populates="initiative", cascade="all, delete-orphan")
    blockers = relationship("Blocker", back_populates="initiative", cascade="all, delete-orphan")
    stakeholders = relationship("Stakeholder", back_populates="initiative", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="initiative", cascade="all, delete-orphan")

    # Downstream dependencies: where this initiative is the TARGET (depends on source)
    upstream_dependencies = relationship(
        "Dependency",
        foreign_keys="Dependency.target_initiative_id",
        back_populates="target_initiative",
        cascade="all, delete-orphan"
    )
    # Upstream dependencies: where this initiative is the SOURCE (blocks target)
    downstream_dependencies = relationship(
        "Dependency",
        foreign_keys="Dependency.source_initiative_id",
        back_populates="source_initiative",
        cascade="all, delete-orphan"
    )


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    target_date = Column(Date, nullable=False)
    actual_date = Column(Date, nullable=True)
    status = Column(String(50), default="PENDING")  # DONE, IN_PROGRESS, DELAYED, AT_RISK, PENDING
    delay_days = Column(Integer, default=0)
    order_index = Column(Integer, default=0)

    initiative = relationship("Initiative", back_populates="milestones")


class KPI(Base):
    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    unit = Column(String(50), default="%")
    trend = Column(String(50), default="FLAT")       # UP, DOWN, FLAT
    is_higher_better = Column(Boolean, default=True)
    history = Column(JSON, default=list)            # list of recent data points: [val1, val2, val3]

    initiative = relationship("Initiative", back_populates="kpis")


class Blocker(Base):
    __tablename__ = "blockers"

    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(50), default="MEDIUM")   # LOW, MEDIUM, HIGH, CRITICAL
    owner = Column(String(255), nullable=False)
    status = Column(String(50), default="OPEN")       # OPEN, IN_PROGRESS, RESOLVED
    days_open = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    initiative = relationship("Initiative", back_populates="blockers")


class Dependency(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True, index=True)
    source_initiative_id = Column(Integer, ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    target_initiative_id = Column(Integer, ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    dependency_type = Column(String(50), default="PREREQUISITE")  # PREREQUISITE, SHARED_RESOURCE, API_INTEGRATION, COMPLIANCE
    status = Column(String(50), default="ACTIVE")                 # ACTIVE, RESOLVED
    impact_severity = Column(String(50), default="HIGH")          # CRITICAL, HIGH, MEDIUM, LOW

    source_initiative = relationship("Initiative", foreign_keys=[source_initiative_id], back_populates="downstream_dependencies")
    target_initiative = relationship("Initiative", foreign_keys=[target_initiative_id], back_populates="upstream_dependencies")


class Stakeholder(Base):
    __tablename__ = "stakeholders"

    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    team = Column(String(100), nullable=False)
    role = Column(String(100), default="Stakeholder") # Executive Sponsor, Product Lead, Tech Lead, Ops Lead

    initiative = relationship("Initiative", back_populates="stakeholders")


class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    initiative_id = Column(Integer, ForeignKey("initiatives.id", ondelete="CASCADE"), nullable=False, index=True)
    risk_type = Column(String(100), default="OPERATIONAL")
    severity = Column(String(50), default="MEDIUM")   # LOW, MEDIUM, HIGH, CRITICAL
    score = Column(Float, default=0.0)
    reason = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    initiative = relationship("Initiative", back_populates="risks")
