import heapq
import itertools
from typing import Dict, List

from state.state_representation import ScheduleState
from cost.cost_function import compute_state_cost
from heuristics.heuristics import heuristic

# Tie-breaker counter for heap (prevents ScheduleState comparison)
_counter = itertools.count()


def generate_successors(
    state: ScheduleState,
    tasks_info: Dict[str, Dict],
    daily_capacity: float,
    max_days: int
) -> List[ScheduleState]:
    """
    Generate valid next states by assigning hours to tasks day by day.
    """

    successors = []

    # Determine current day (start from day 1)
    current_day = max(state.schedule.keys(), default=0) + 1
    if current_day > max_days:
        return successors

    # Remaining capacity for the day
    used = state.daily_usage.get(current_day, 0)
    remaining_capacity = daily_capacity - used
    if remaining_capacity <= 0:
        return successors

    # Try assigning work to each unfinished task
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


def astar_search(
    initial_state: ScheduleState,
    tasks_info: Dict[str, Dict],
    daily_capacity: float,
    max_days: int = 30
) -> ScheduleState:
    """
    Perform A* search to find the optimal schedule.
    """

    open_list = []
    closed_set = set()

    g_initial = 0
    h_initial = heuristic(initial_state, tasks_info, daily_capacity)
    f_initial = g_initial + h_initial

    # Push with tie-breaker
    heapq.heappush(
        open_list,
        (f_initial, g_initial, next(_counter), initial_state)
    )

    while open_list:
        f, g, _, current_state = heapq.heappop(open_list)

        # Goal check
        if current_state.is_goal_state():
            return current_state

        # Avoid revisiting identical states
        state_key = str(current_state.schedule)
        if state_key in closed_set:
            continue
        closed_set.add(state_key)

        successors = generate_successors(
            current_state, tasks_info, daily_capacity, max_days
        )

        for next_state in successors:
            g_next = compute_state_cost(next_state, tasks_info)
            h_next = heuristic(next_state, tasks_info, daily_capacity)
            f_next = g_next + h_next

            heapq.heappush(
                open_list,
                (f_next, g_next, next(_counter), next_state)
            )

    # If no solution found, return best effort
    return initial_state