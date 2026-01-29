from typing import Dict
from state.state_representation import ScheduleState

PRIORITY_PENALTY = {
    "High": 5,
    "Medium": 3,
    "Low": 1
}

def compute_priority_cost(task: Dict, day: int) -> float:
    return PRIORITY_PENALTY.get(task["priority"], 1) * day

def compute_soft_deadline_cost(task: Dict, day: int) -> float:
    if task["deadline_type"] == "SOFT" and day > task["deadline_days"]:
        return (day - task["deadline_days"]) * 4
    return 0.0

def compute_inefficiency_cost(task: Dict, day: int) -> float:
    urgency = task["urgency_score"]
    return urgency * day * 0.1

def compute_state_cost(state: ScheduleState, tasks_info: Dict[str, Dict]) -> float:
    total_cost = 0.0

    for day, assignments in state.schedule.items():
        for task_name, _ in assignments:
            task = tasks_info[task_name]
            total_cost += compute_priority_cost(task, day)
            total_cost += compute_soft_deadline_cost(task, day)
            total_cost += compute_inefficiency_cost(task, day)

    return total_cost