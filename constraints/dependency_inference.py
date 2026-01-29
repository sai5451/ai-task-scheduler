from typing import Dict, List, Tuple


def should_precede(task_a: Dict, task_b: Dict) -> bool:
    """
    Decide whether task_a should be done before task_b
    using logical rules.
    """

    # Rule 1: Hard deadlines first
    if task_a["deadline_type"] == "HARD" and task_b["deadline_type"] == "SOFT":
        return True
    if task_b["deadline_type"] == "HARD" and task_a["deadline_type"] == "SOFT":
        return False

    # Rule 2: Higher priority first
    priority_rank = {"High": 3, "Medium": 2, "Low": 1}
    if priority_rank[task_a["priority"]] > priority_rank[task_b["priority"]]:
        return True
    if priority_rank[task_a["priority"]] < priority_rank[task_b["priority"]]:
        return False

    # Rule 3: Preparation tasks first
    if task_a["has_preparation_constraint"] and not task_b["has_preparation_constraint"]:
        return True
    if task_b["has_preparation_constraint"] and not task_a["has_preparation_constraint"]:
        return False

    # Rule 4: Earlier deadline first
    if task_a["deadline_days"] < task_b["deadline_days"]:
        return True
    if task_a["deadline_days"] > task_b["deadline_days"]:
        return False

    # Rule 5: Higher urgency score first
    return task_a["urgency_score"] > task_b["urgency_score"]


def infer_dependencies(tasks: List[Dict]) -> List[Tuple[str, str]]:
    """
    Infer precedence relationships between tasks.
    Returns a list of (task_before, task_after) pairs.
    """

    dependencies = []

    for i in range(len(tasks)):
        for j in range(len(tasks)):
            if i == j:
                continue

            task_a = tasks[i]
            task_b = tasks[j]

            if should_precede(task_a, task_b):
                dependencies.append((task_a["name"], task_b["name"]))

    return dependencies