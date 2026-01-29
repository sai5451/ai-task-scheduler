from typing import Dict
from state.state_representation import ScheduleState


def format_schedule(state: ScheduleState) -> str:
    """
    Format the day-wise schedule.
    """
    lines = ["\n=== FINAL SCHEDULE ==="]

    for day in sorted(state.schedule.keys()):
        lines.append(f"\nDay {day}:")
        for task_name, hours in state.schedule[day]:
            lines.append(f"  - {task_name}: {hours} hours")

    return "\n".join(lines)


def format_task_status(tasks_info: Dict[str, Dict], state: ScheduleState) -> str:
    """
    Show completion status of tasks.
    """
    lines = ["\n=== TASK STATUS ==="]

    for task_name, task in tasks_info.items():
        remaining = state.remaining_tasks.get(task_name, 0)
        status = "Completed" if remaining <= 0 else f"Remaining: {remaining}h"
        lines.append(f"- {task_name}: {status}")

    return "\n".join(lines)


def format_warnings(feasibility_result: Dict) -> str:
    """
    Format warnings and suggestions.
    """
    lines = ["\n=== WARNINGS & SUGGESTIONS ==="]

    warnings = feasibility_result.get("warnings", [])
    suggestions = feasibility_result.get("suggestions", [])

    if not warnings:
        lines.append("No constraint violations detected.")
    else:
        lines.append("\nWarnings:")
        for w in warnings:
            lines.append(f"- {w}")

    if suggestions:
        lines.append("\nSuggestions:")
        for s in suggestions:
            lines.append(f"- {s}")

    return "\n".join(lines)


def format_explanation(explanation_text: str) -> str:
    """
    Format explanation output.
    """
    return "\n=== EXPLANATION ===\n" + explanation_text


def format_final_output(
    state: ScheduleState,
    tasks_info: Dict[str, Dict],
    feasibility_result: Dict,
    explanation_text: str
) -> str:
    """
    Combine all outputs into one final report.
    """

    parts = []
    parts.append(format_schedule(state))
    parts.append(format_task_status(tasks_info, state))
    parts.append(format_warnings(feasibility_result))
    parts.append(format_explanation(explanation_text))

    return "\n\n".join(parts)