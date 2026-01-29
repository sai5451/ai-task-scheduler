from typing import Dict
from state.state_representation import ScheduleState


def remaining_workload_heuristic(state: ScheduleState, daily_capacity: float) -> float:
    """
    Estimate remaining days needed based on unfinished work.
    """
    remaining_hours = sum(max(0, h) for h in state.remaining_tasks.values())
    if daily_capacity == 0:
        return float("inf")
    return remaining_hours / daily_capacity


def deadline_pressure_heuristic(state: ScheduleState, tasks_info: Dict[str, Dict]) -> float:
    """
    Estimate penalty based on how close tasks are to deadlines.
    """
    pressure = 0.0
    current_day = max(state.schedule.keys(), default=0)

    for task_name, remaining_hours in state.remaining_tasks.items():
        if remaining_hours <= 0:
            continue

        task = tasks_info[task_name]
        days_left = task["deadline_days"] - current_day

        if days_left <= 0:
            # Deadline already reached or passed
            pressure += remaining_hours * 2
        else:
            pressure += remaining_hours / days_left

    return pressure


def urgency_heuristic(state: ScheduleState, tasks_info: Dict[str, Dict]) -> float:
    """
    Estimate urgency of unfinished tasks.
    """
    urgency_score = 0.0
    for task_name, remaining_hours in state.remaining_tasks.items():
        if remaining_hours <= 0:
            continue

        task = tasks_info[task_name]
        urgency_score += task["urgency_score"] * remaining_hours

    return urgency_score * 0.1


def heuristic(state: ScheduleState, tasks_info: Dict[str, Dict], daily_capacity: float) -> float:
    """
    Final heuristic function h(n).
    Uses max() to stay admissible and optimistic.
    """

    h1 = remaining_workload_heuristic(state, daily_capacity)
    h2 = deadline_pressure_heuristic(state, tasks_info)
    h3 = urgency_heuristic(state, tasks_info)

    return max(h1, h2, h3)