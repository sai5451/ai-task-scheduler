from typing import Dict, List
from input.input_schema import TaskInput, AvailabilityInput, UserInput

# ---------------- FIXED MAPPINGS ---------------- #
# Deterministic and explainable

LENGTH_TO_HOURS = {
    "Very Short": 1,
    "Short": 2,
    "Medium": 4,
    "Long": 6
}

ENERGY_TO_HOURS = {
    "Tired": 2,
    "Normal": 3,
    "Energetic": 5
}


# ---------------- TASK INTERPRETATION ---------------- #

def interpret_task(task: TaskInput) -> Dict:
    """
    Convert TaskInput into a numeric task model.
    """

    # Determine total hours required
    if task.approximate_hours is not None:
        total_hours = float(task.approximate_hours)
    else:
        total_hours = LENGTH_TO_HOURS[task.descriptive_length]

    return {
        "name": task.name,
        "priority": task.priority,
        "deadline_days": task.deadline_days,
        "strict_deadline": task.strict_deadline,
        "total_hours": total_hours,
        "task_type": task.task_type
    }


# ---------------- AVAILABILITY INTERPRETATION ---------------- #

def interpret_availability(avail: AvailabilityInput) -> Dict:
    """
    Convert AvailabilityInput into numeric daily capacity.
    """

    energy_limit = ENERGY_TO_HOURS[avail.energy_level]

    # work_until now represents DAILY HOURS (1–8)
    time_limit = int(avail.work_until)

    daily_capacity = min(energy_limit, time_limit)

    return {
        "daily_capacity": daily_capacity,
        "blocked_days": avail.blocked_days or []
    }


# ---------------- USER INPUT INTERPRETATION ---------------- #

def interpret_user_input(user_input: UserInput) -> Dict:
    """
    Convert full user input into a numeric model for the planner.
    """

    interpreted_tasks = [
        interpret_task(task) for task in user_input.tasks
    ]

    interpreted_availability = interpret_availability(
        user_input.availability
    )

    return {
        "tasks": interpreted_tasks,
        "availability": interpreted_availability
    }