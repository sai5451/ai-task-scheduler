Project Objective :
-Design a classical AI task planner for students that:
-Schedules tasks efficiently with no wasted time
-Assigns exact study hours per task per day
-Respects deadlines, priorities, and personal limits
-Warns the user only when constraints cannot be satisfied
-Remains fully explainable and deterministic
.
.
WORK FLOW :
User launches gui_app.py
        |
        v
User enters tasks + limits in GUI
        |
        v
GUI Controller collects raw input
        |
        v
Input Validation Layer
(check missing / invalid values)
        |
        v
Input Mapping & Interpretation
(words → numbers, labels → weights)
        |
        v
Initial ScheduleState created
(nothing scheduled yet)
        |
        v
AI Planner Selected (A*)
        |
        v
State-Space Search Begins
(A* expands states)
        |
        v
Constraint Checking
(deadlines, resources, priorities)
        |
        v
Feasibility Pruning
(impossible states dropped)
        |
        v
Goal State Reached
(all tasks scheduled)
        |
        v
Explanation Trace Generated
(why each decision was made)
        |
        v
Formatted Output Returned
(schedule + reasoning)
        |
        v
GUI displays final schedule
.
.
.
Strict deadline = hard constraint
-Task must finish on or before deadline
-Non‑strict deadline = soft constraint
-Can cross deadline with penalty

5. Efficiency Rules (Mandatory)
Scheduling always starts from Day 1
Tasks are packed as early as possible
No idle time if tasks and capacity exist
High‑priority + strict‑deadline tasks scheduled first
Planner assigns exact hours per task per day

6. Suggestions & Warnings
Shown only if:
A strict deadline cannot be met, or
Resource limits make completion impossible
Suggestions may include:
Increase daily availability
Reduce task length
Relax deadline strictness
Extend deadline
