from dataclasses import dataclass
from typing import Optional, List

@dataclass
class TaskInput:
    """
    Represents a single task provided by the user.
    Raw input only — no inference here.
    """

    name: str
    priority: str                 # "High" | "Medium" | "Low"
    deadline_days: int             # >= 1
    strict_deadline: bool

    # Task length (choose ONE)
    approximate_hours: Optional[float] = None
    descriptive_length: Optional[str] = None
    # {"Very Short", "Short", "Medium", "Long"}

    # Optional metadata (non‑constraining)
    task_type: Optional[str] = None


@dataclass
class AvailabilityInput:
    """
    Availability in terms of DAILY HOURS, not time-of-day.
    """

    energy_level: str              # "Tired" | "Normal" | "Energetic"
    work_until: int                # daily hours (1–8)
    blocked_days: List[int]


@dataclass
class UserInput:
    """
    Complete user input.
    """
    tasks: List[TaskInput]
    availability: AvailabilityInput
