import heapq
from typing import Dict, List

from state.state_representation import ScheduleState
from heuristics.heuristics import heuristic


def generate_successors(
    state: ScheduleState,
    tasks_info: Dict[str, Dict],
    daily_capacity: float,
    max_days: int
) -> List[ScheduleState]:
    """
    Same successor generation logic as A* and UCS.
    """

    successors = []

    current_day = max(state.schedule.keys(), default=0) + 1
    if current_day > max_days:
        return successors

    used = state.daily_usage.get(current_day, 0)
    remaining_capacity = daily_capacity - used
    if remaining_capacity <= 0:
        return successors

    for task_name, remaining_hours in state.remaining_tasks.items():
        if remaining_hours <= 0:
            continue

        hours_to_assign = min(remaining_hours, remaining_capacity)

        new_state = state.copy()
        new_state.parent = state
        new_state.action = f"Assign {hours_to_assign}h to {task_name} on Day {current_day}"

        new_state.add_task_to_day(current_day, task_name, hours_to_assign)

        successors.append(new_state)

    return successors


def greedy_search(
    initial_state: ScheduleState,
    tasks_info: Dict[str, Dict],
    daily_capacity: float,
    max_days: int = 30
) -> ScheduleState:
    """
    Greedy Best-First Search: selects states with minimum h(n).
    """

    open_list = []
    closed_set = set()

    h_initial = heuristic(initial_state, tasks_info, daily_capacity)
    heapq.heappush(open_list, (h_initial, initial_state))

    while open_list:
        h, current_state = heapq.heappop(open_list)

        # Goal check
        if current_state.is_goal_state():
            return current_state

        state_key = str(current_state.schedule)
        if state_key in closed_set:
            continue
        closed_set.add(state_key)

        successors = generate_successors(
            current_state, tasks_info, daily_capacity, max_days
        )

        for next_state in successors:
            h_next = heuristic(next_state, tasks_info, daily_capacity)
            heapq.heappush(open_list, (h_next, next_state))

    return initial_state