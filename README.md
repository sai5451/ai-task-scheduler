Project Objective
Design a classical AI task planner for students that:
Schedules tasks efficiently with no wasted time
Assigns exact study hours per task per day
Respects deadlines, priorities, and personal limits
Warns the user only when constraints cannot be satisfied
Remains fully explainable and deterministic

User‑Facing Input Requirements :

A. Task Details (per task)
The user provides:
Task name
Priority: High / Medium / Low
Deadline: Number of days from today
Deadline strictness: Yes / No
Task length (choose ONE option):
Option 1: Approximate hours (e.g., 1.5 h, 3 h, 6 h)
Option 2: Very Short / Short / Medium / Long
Task type (optional): Study / Assignment / Revision / Reading / Practice
Needs preparation? (Yes / No)
Uses exclusive resource? (Yes / No)
The user never specifies dependencies or daily hours.

B. Availability & Limits
Daily energy level: Tired / Normal / Energetic
Can work until: 7 PM / 9 PM / 11 PM
Blocked days (optional)

3. Internal System Logic (Fixed)

A. Time Mapping
If user gives hours → used directly
If user gives descriptive length → mapped internally:
Very Short → 1 hour
Short → 2 hours
Medium → 4 hours
Long → 6 hours

B. Daily Capacity Mapping
Tired → 2 hours/day
Normal → 3 hours/day
Energetic → 5 hours/day
(capped by “work until” time)

4. Deadline Handling
Strict deadline = hard constraint
Task must finish on or before deadline
Non‑strict deadline = soft constraint
Can cross deadline with penalty

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


📄 FINAL INPUT–OUTPUT EXAMPLE PAGE

INPUT (Student provides)
Tasks
History studying
Priority: Low
Deadline: 5 days
Deadline strictness: Yes
Task length: Long



Math assignment
Priority: High
Deadline: 2 days
Deadline strictness: Yes
Task length: 4 hours



English reading
Priority: Low
Deadline: 6 days
Deadline strictness: No
Task length: Short




Availability
Energy level: Normal
Can work till: 9 PM
Blocked days: None

OUTPUT (System produces)

Planned Schedule (exact hours)
Day 1
Math assignment — 3 hours
Day 2
Math assignment — 1 hour
History studying — 2 hours
Day 3
History studying — 3 hours
Day 4
History studying — 1 hour
English reading — 1 hour

LAYERS AND CONCEPTS : 
Input & Validation Layer
→ Problem formulation
(Defining what the AI problem consists of)
Interpretation & Mapping Layer
→ Abstraction & representation
(Converting real‑world input into symbolic/numeric form)
Constraint & Dependency Inference Layer
→ Constraint Satisfaction (CSP)
(Hard vs soft constraints, precedence rules)
State Representation Layer
→ State‑space representation
(How a state and partial solution are defined)
Cost Function Layer
→ Path cost formulation
(Defining g(n) for optimal search)
Heuristic Layer
→ Heuristic design
(Admissible, consistent heuristic functions)
Planning & Search Layer
→ Informed & uninformed search
(A*, UCS, Greedy Best‑First)
Feasibility & Warning Layer
→ Constraint checking & pruning
(Detecting dead‑ends and impossible states)
Explanation Layer
→ Symbolic reasoning & explainable AI
(Rule‑based explanation, not learning)
Output Assembly Layer
→ Action execution & reporting
(Presenting the plan produced by the agent)





FOLDER STRUCTURE : 

task_planner/
│
├── input/
│   ├── input_schema.py
│   └── validator.py
│
├── mapping/
│   └── interpreter.py
│
├── constraints/
│   ├── constraint_rules.py
│   └── dependency_inference.py
│
├── state/
│   └── state_representation.py
│
├── cost/
│   └── cost_function.py
│
├── heuristics/
│   └── heuristics.py
│
├── planner/
│   ├── astar.py
│   ├── ucs.py
│   └── greedy.py
│
├── feasibility/
│   └── feasibility_checker.py
│
├── explanation/
│   └── explanation_engine.py
│
├── output/
│   └── output_formatter.py
│
├── config/
│   └── constants.py
│
└── main.py
|
|
ui/
 ├── gui_app.py          # main GUI application
 ├── gui_layout.py       # layout & widgets
 ├── gui_styles.py       # colors, fonts, spacing
 └── gui_controller.py  # connects GUI ↔ main.py

