from typing import Dict, List
from state.state_representation import ScheduleState


def explain_task_order(tasks_info: Dict[str, Dict]) -> List[str]:
    """
    Explain why some tasks were prioritized over others.
    """
    explanations = []

    sorted_tasks = sorted(
        tasks_info.values(),
        key=lambda t: (-t["urgency_score"], t["deadline_days"])
    )

    if len(sorted_tasks) > 1:
        top_task = sorted_tasks[0]
        explanations.append(
            f"Task '{top_task['name']}' was prioritized because it has higher urgency "
            f"(priority and deadline pressure)."
        )

    return explanations


def explain_task_splitting(state: ScheduleState) -> List[str]:
    """
    Explain why tasks were split across multiple days.
    """
    explanations = []
    task_days = {}

    for day, assignments in state.schedule.items():
        for task_name, _ in assignments:
            task_days.setdefault(task_name, []).append(day)

    for task_name, days in task_days.items():
        if len(days) > 1:
            explanations.append(
                f"Task '{task_name}' was split across multiple days to balance workload "
                f"and respect daily capacity limits."
            )

    return explanations


def explain_deadlines(tasks_info: Dict[str, Dict], state: ScheduleState) -> List[str]:
    """
    Explain how deadlines affected scheduling.
    """
    explanations = []

    for task in tasks_info.values():
        if task["deadline_type"] == "HARD":
            explanations.append(
                f"Task '{task['name']}' was scheduled early because it has a strict deadline."
            )
        else:
            explanations.append(
                f"Task '{task['name']}' was scheduled flexibly because its deadline is not strict."
            )

    return explanations


def explain_efficiency(state: ScheduleState) -> List[str]:
    """
    Explain why no idle time was wasted.
    """
    explanations = []

    total_days = len(state.schedule)
    if total_days > 0:
        explanations.append(
            "The planner avoided idle time by scheduling tasks as early as possible "
            "while respecting daily limits."
        )

    return explanations


def generate_explanation(state: ScheduleState, tasks_info: Dict[str, Dict]) -> str:
    """
    Generate a full human-readable explanation of the schedule.
    """

    explanation_parts = []

    explanation_parts += explain_task_order(tasks_info)
    explanation_parts += explain_task_splitting(state)
    explanation_parts += explain_deadlines(tasks_info, state)
    explanation_parts += explain_efficiency(state)

    if not explanation_parts:
        return "The schedule was generated efficiently based on given constraints."

    return "\n".join("- " + e for e in explanation_parts)