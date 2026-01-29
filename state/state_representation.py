from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import copy

@dataclass
class ScheduleState:
    """
    Represents a partial or complete schedule.
    """

    schedule: Dict[int, List[Tuple[str, float]]] = field(default_factory=dict)
    remaining_tasks: Dict[str, float] = field(default_factory=dict)
    daily_usage: Dict[int, float] = field(default_factory=dict)
    cost: float = 0.0

    parent: Optional["ScheduleState"] = None
    action: Optional[str] = None

    def is_goal_state(self) -> bool:
        return all(hours <= 0 for hours in self.remaining_tasks.values())

    def copy(self) -> "ScheduleState":
        return ScheduleState(
            schedule=copy.deepcopy(self.schedule),
            remaining_tasks=copy.deepcopy(self.remaining_tasks),
            daily_usage=copy.deepcopy(self.daily_usage),
            cost=self.cost,
            parent=self.parent,
            action=self.action
        )

    def add_task_to_day(self, day: int, task_name: str, hours: float) -> None:
        if day not in self.schedule:
            self.schedule[day] = []

        self.schedule[day].append((task_name, hours))
        self.remaining_tasks[task_name] -= hours
        self.daily_usage[day] = self.daily_usage.get(day, 0) + hours