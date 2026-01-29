"""
Global constants used across the task planner system.
This file centralizes fixed rules and mappings.
"""

# -----------------------------
# Task Length Mapping (if user uses adjectives)
# -----------------------------
TASK_LENGTH_TO_HOURS = {
    "Very Short": 1,
    "Short": 2,
    "Medium": 4,
    "Long": 6
}

# -----------------------------
# Priority Weights (used in cost & urgency)
# -----------------------------
PRIORITY_WEIGHTS = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

PRIORITY_PENALTY = {
    "High": 5,
    "Medium": 3,
    "Low": 1
}

# -----------------------------
# Energy Level → Daily Capacity
# -----------------------------
ENERGY_TO_HOURS = {
    "Tired": 2,
    "Normal": 3,
    "Energetic": 5
}

# -----------------------------
# Work-Until Time → Hour Limit
# -----------------------------
TIME_TO_HOURS = {
    "7 PM": 2,
    "9 PM": 3,
    "11 PM": 5
}

# -----------------------------
# Planning Limits
# -----------------------------
DEFAULT_MAX_DAYS = 30   # maximum planning horizon
INEFFICIENCY_WEIGHT = 0.1
SOFT_DEADLINE_PENALTY = 4

# -----------------------------
# Allowed Input Values
# -----------------------------
ALLOWED_PRIORITIES = {"High", "Medium", "Low"}
ALLOWED_LENGTHS = {"Very Short", "Short", "Medium", "Long"}
ALLOWED_ENERGY_LEVELS = {"Tired", "Normal", "Energetic"}
ALLOWED_WORK_TIMES = {"7 PM", "9 PM", "11 PM"}