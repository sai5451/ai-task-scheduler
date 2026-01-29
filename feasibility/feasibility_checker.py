from typing import Dict, List, Tuple


def check_strict_deadlines(tasks: List[Dict], daily_capacity: float) -> List[str]:
    """
    Check if strict deadlines can be met with available time.
    Returns warning messages.
    """
    warnings = []

    for task in tasks:
        if task["deadline_type"] == "HARD":
            max_possible_hours = task["deadline_days"] * daily_capacity

            if task["total_hours"] > max_possible_hours:
                warnings.append(
                    f"Strict deadline violation risk: "
                    f"Task '{task['name']}' requires {task['total_hours']}h "
                    f"but only {max_possible_hours}h available before deadline."
                )

    return warnings


def check_total_feasibility(tasks: List[Dict], daily_capacity: float, max_days: int) -> List[str]:
    """
    Check if total workload is feasible within planning horizon.
    """
    warnings = []

    total_required_hours = sum(task["total_hours"] for task in tasks)
    total_available_hours = daily_capacity * max_days

    if total_required_hours > total_available_hours:
        warnings.append(
            f"Overall infeasibility: Total required hours ({total_required_hours}) "
            f"exceed available hours ({total_available_hours})."
        )

    return warnings


def generate_suggestions(tasks: List[Dict], daily_capacity: float) -> List[str]:
    """
    Suggest ways to resolve infeasibility.
    """
    suggestions = []

    for task in tasks:
        if task["deadline_type"] == "HARD":
            required_per_day = task["total_hours"] / task["deadline_days"]

            if required_per_day > daily_capacity:
                suggestions.append(
                    f"For task '{task['name']}', consider:\n"
                    f"- Increasing daily availability to ~{required_per_day:.2f}h/day\n"
                    f"- Reducing task length\n"
                    f"- Relaxing deadline strictness"
                )

    return suggestions


def feasibility_check(tasks: List[Dict], daily_capacity: float, max_days: int = 30) -> Dict:
    """
    Main feasibility checker.
    Returns warnings and suggestions.
    """

    warnings = []
    suggestions = []

    warnings += check_strict_deadlines(tasks, daily_capacity)
    warnings += check_total_feasibility(tasks, daily_capacity, max_days)

    if warnings:
        suggestions = generate_suggestions(tasks, daily_capacity)

    return {
        "warnings": warnings,
        "suggestions": suggestions
    }