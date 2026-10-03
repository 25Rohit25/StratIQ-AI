from datetime import timedelta, date
from typing import Dict, Any, List, Set
from sqlalchemy.orm import Session
from app.models import Initiative, Dependency, Stakeholder, KPI

def simulate_change_impact(initiative_id: int, simulated_delay_days: int, db: Session, reason: str = "") -> Dict[str, Any]:
    """
    Performs topological / BFS downstream dependency traversal to determine ripple effects of a delay.
    """
    source_init = db.query(Initiative).filter(Initiative.id == initiative_id).first()
    if not source_init:
        return {
            "error": "Source initiative not found",
            "impacted_initiatives": []
        }

    # Queue for BFS: (initiative_id, depth, path)
    queue = [(initiative_id, 1)]
    visited: Set[int] = {initiative_id}
    impacted_list = []

    while queue:
        curr_id, depth = queue.pop(0)

        # Find all downstream dependencies where curr_id is the source
        downstream_deps = db.query(Dependency).filter(
            Dependency.source_initiative_id == curr_id,
            Dependency.status == "ACTIVE"
        ).all()

        for dep in downstream_deps:
            target = dep.target_initiative
            if not target:
                continue

            target_id = target.id
            if target_id not in visited:
                visited.add(target_id)
                queue.append((target_id, depth + 1))

                # Calculate projected dates and risks
                orig_target = target.target_date or date.today()
                # Cascade delay may attenuate or compound depending on depth
                effective_delay = max(simulated_delay_days - (depth - 1) * 2, 3)
                new_projected = orig_target + timedelta(days=effective_delay)

                # Project new risk level
                orig_risk = target.risk_level or "HEALTHY"
                if effective_delay >= 14 or orig_risk == "AT_RISK":
                    proj_risk = "CRITICAL"
                elif effective_delay >= 7 or orig_risk == "WATCH":
                    proj_risk = "AT_RISK"
                else:
                    proj_risk = "WATCH"

                affected_kpis = [k.name for k in target.kpis]
                affected_stakeholders = [f"{s.name} ({s.role}, {s.team})" for s in target.stakeholders]

                impacted_list.append({
                    "initiative_id": target.id,
                    "name": target.name,
                    "owner": target.owner,
                    "original_target_date": orig_target,
                    "new_projected_date": new_projected,
                    "direct_or_cascading": "DIRECT" if depth == 1 else f"CASCADING_LEVEL_{depth}",
                    "original_risk_level": orig_risk,
                    "projected_risk_level": proj_risk,
                    "affected_kpis": affected_kpis[:3],
                    "affected_stakeholders": affected_stakeholders[:3]
                })

    # Generate synthesis
    total_affected = len(impacted_list)
    critical_delayed = total_affected > 0

    if total_affected == 0:
        summary = f"Simulating a {simulated_delay_days}-day delay on '{source_init.name}' produces isolated impact: no downstream strategic initiatives depend directly on this program."
        mitigations = [
            "Maintain current delivery schedule without cross-team alerting.",
            "Reallocate any slack resources to upstream critical programs."
        ]
    else:
        names = ", ".join([f"'{item['name']}'" for item in impacted_list[:3]])
        if total_affected > 3:
            names += f" and {total_affected - 3} other initiatives"

        summary = (
            f"A {simulated_delay_days}-day slip on '{source_init.name}' creates a cascading delay across {total_affected} "
            f"downstream programs including {names}. Key milestones will slip past scheduled quarterly windows."
        )
        mitigations = [
            f"Implement decoupling / API mocking for {impacted_list[0]['name']} to allow frontend teams to progress in parallel.",
            f"Notify executive sponsors and schedule an emergency scope triage to preserve release deadlines.",
            f"Review Q4 commitments for affected metrics: {', '.join(impacted_list[0]['affected_kpis'] or ['Revenue Targets'])}."
        ]

    return {
        "source_initiative_id": source_init.id,
        "source_initiative_name": source_init.name,
        "simulated_delay_days": simulated_delay_days,
        "total_affected_initiatives": total_affected,
        "impacted_initiatives": impacted_list,
        "critical_path_delayed": critical_delayed,
        "summary": summary,
        "mitigation_recommendations": mitigations
    }
