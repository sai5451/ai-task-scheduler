from input.validator import validate_user_input
from mapping.interpreter import interpret_user_input
from constraints.constraint_rules import infer_constraints
from state.state_representation import ScheduleState
from planner.astar import astar_search
from feasibility.feasibility_checker import feasibility_check
from explanation.explanation_engine import generate_explanation
from output.output_formatter import format_final_output


def run_planner(user_input):
    """
    Core AI planner pipeline.
    Fully requirement-aligned and constraint-aware.
    """

    # 1. Validate raw user input
    validate_user_input(user_input)

    # 2. Interpret user-friendly input into numeric model
    interpreted = interpret_user_input(user_input)

    # 3. Infer constraints and enrich tasks
    tasks_with_constraints = infer_constraints(interpreted["tasks"])
    tasks_info = {t["name"]: t for t in tasks_with_constraints}

    daily_capacity = interpreted["availability"]["daily_capacity"]

    # 4. FEASIBILITY CHECK (STRICT DEADLINES ONLY BLOCK)
    feasibility_result = feasibility_check(tasks_with_constraints, daily_capacity)

    strict_blocking = any(
        "Strict deadline violation risk" in warning
        for warning in feasibility_result["warnings"]
    )

    if strict_blocking:
        explanation_text = (
            "The planner could not generate a schedule because one or more "
            "strict deadlines cannot be satisfied with the given constraints."
        )

        return format_final_output(
            state=ScheduleState(remaining_tasks={}),
            tasks_info=tasks_info,
            feasibility_result=feasibility_result,
            explanation_text=explanation_text
        )

    # 5. Build initial state (only if feasible)
    initial_state = ScheduleState(
        remaining_tasks={t["name"]: t["total_hours"] for t in tasks_info.values()}
    )

    # 6. Run A* planner
    final_state = astar_search(
        initial_state=initial_state,
        tasks_info=tasks_info,
        daily_capacity=daily_capacity
    )

    # 7. Generate explanation
    explanation_text = generate_explanation(final_state, tasks_info)

    # 8. Format and return final output
    return format_final_output(
        state=final_state,
        tasks_info=tasks_info,
        feasibility_result=feasibility_result,
        explanation_text=explanation_text
    )