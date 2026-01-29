from typing import Dict, List

def classify_deadline(task: Dict) -> str:
    return "HARD" if task["strict_deadline"] else "SOFT"

def priority_weight(priority: str) -> int:
    return {"High": 3, "Medium": 2, "Low": 1}.get(priority, 1)

def compute_urgency(task: Dict) -> float:
    return (
        (1 / task["deadline_days"])
        * priority_weight(task["priority"])
        * task["total_hours"]
    )

def infer_constraints(tasks: List[Dict]) -> List[Dict]:
    enriched = []

    for task in tasks:
        t = task.copy()
        t["deadline_type"] = classify_deadline(task)
        t["urgency_score"] = compute_urgency(task)

        # Explicit flags (used by planner)
        t["has_preparation_constraint"] = False
        t["has_resource_constraint"] = False

        enriched.append(t)

    return enriched