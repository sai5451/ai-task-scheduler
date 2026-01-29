from typing import List
from input.input_schema import TaskInput, AvailabilityInput, UserInput


class InputValidationError(Exception):
    """Custom exception for input validation errors."""
    pass


def validate_task(task: TaskInput) -> None:
    # 1. Name check
    if not task.name or not isinstance(task.name, str):
        raise InputValidationError("Task name must be a non-empty string.")

    # 2. Priority check
    allowed_priorities = {"High", "Medium", "Low"}
    if task.priority not in allowed_priorities:
        raise InputValidationError(
            f"Invalid priority '{task.priority}'. Allowed: {allowed_priorities}"
        )

    # 3. Deadline check
    if not isinstance(task.deadline_days, int) or task.deadline_days < 1:
        raise InputValidationError("Deadline must be an integer >= 1 day.")

    # 4. Task length rule: either hours OR descriptive length must be provided
    if task.approximate_hours is None and task.descriptive_length is None:
        raise InputValidationError(
            f"Task '{task.name}' must have either approximate_hours or descriptive_length."
        )

    # 5. If approximate hours is given, it must be positive
    if task.approximate_hours is not None:
        if not isinstance(task.approximate_hours, (int, float)) or task.approximate_hours <= 0:
            raise InputValidationError(
                f"Task '{task.name}': approximate_hours must be a positive number."
            )

    # 6. If descriptive length is given, it must be valid
    if task.descriptive_length is not None:
        allowed_lengths = {"Very Short", "Short", "Medium", "Long"}
        if task.descriptive_length not in allowed_lengths:
            raise InputValidationError(
                f"Task '{task.name}': invalid descriptive_length. Allowed: {allowed_lengths}"
            )


def validate_availability(avail: AvailabilityInput) -> None:
    # 1. Energy level check
    allowed_energy = {"Tired", "Normal", "Energetic"}
    if avail.energy_level not in allowed_energy:
        raise InputValidationError(
            f"Invalid energy level '{avail.energy_level}'. Allowed: {allowed_energy}"
        )

    # 2. Work-until time check
    def validate_availability(avail):
        # Energy level validation (keep as is)
        if avail.energy_level not in {"Tired", "Normal", "Energetic"}:
            raise InputValidationError(
            f"Invalid energy level '{avail.energy_level}'"
        )

    # Daily hours validation (NEW, CORRECT)
    try:
        hours = int(avail.work_until)
    except ValueError:
        raise InputValidationError(
            f"Daily work hours must be an integer between 1 and 8"
        )

    if not (1 <= hours <= 8):
        raise InputValidationError(
            f"Daily work hours must be between 1 and 8"
        )


    # 3. Blocked days check (optional)
    if avail.blocked_days is not None:
        if not isinstance(avail.blocked_days, list):
            raise InputValidationError("blocked_days must be a list of strings.")


def validate_user_input(user_input: UserInput) -> None:
    # Validate all tasks
    if not user_input.tasks or len(user_input.tasks) == 0:
        raise InputValidationError("At least one task must be provided.")

    for task in user_input.tasks:
        validate_task(task)

    # Validate availability
    validate_availability(user_input.availability)
