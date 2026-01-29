import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk

from input.input_schema import TaskInput, AvailabilityInput, UserInput
from main import run_planner

# ---------------- VISUAL CONFIG ---------------- #

BG_BLUE = "#d9e9f7"
PANEL_BLUE = "#eaf3fb"
TEXT_COLOR = "#000000"

FONT_TITLE = ("Refuel", 15, "bold")
FONT_HEADER = ("Refuel", 11, "bold")
FONT_TEXT = ("Refuel", 9)


class TaskPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Student Task Planner")
        self.root.geometry("1100x600")
        self.root.configure(bg=BG_BLUE)

        self.tasks = []

        self.build_layout()

    # ---------------- LAYOUT ---------------- #

    def build_layout(self):
        tk.Label(
            self.root,
            text="AI Student Task Planner",
            bg=BG_BLUE,
            fg=TEXT_COLOR,
            font=FONT_TITLE
        ).pack(pady=5)

        container = tk.Frame(self.root, bg=BG_BLUE)
        container.pack(fill="both", expand=True, padx=15, pady=5)

        self.build_input_panel(container)
        self.build_output_panel(container)

    # ---------------- INPUT PANEL ---------------- #

    def build_input_panel(self, parent):
        self.input_panel = tk.Frame(parent, bg=PANEL_BLUE)
        self.input_panel.pack(side="left", fill="both", expand=True, padx=8)

        tk.Label(
            self.input_panel, text="INPUT",
            bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_HEADER
        ).pack(pady=3)

        task_box = tk.LabelFrame(
            self.input_panel, text="Task Details",
            bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_TEXT
        )
        task_box.pack(fill="x", padx=8, pady=4)

        self.task_name = tk.StringVar()
        self.priority = tk.StringVar(value="Medium")
        self.deadline = tk.StringVar()
        self.strict = tk.BooleanVar()

        self.length_mode = tk.StringVar(value="hours")
        self.hours = tk.StringVar()
        self.length = tk.StringVar()  # 🔴 NO "None"

        self.task_type = tk.StringVar(value="Study")

        self._row(task_box, "Task Name", self.task_name, 0)
        self._combo(task_box, "Priority", self.priority,
                    ["High", "Medium", "Low"], 1)
        self._row(task_box, "Deadline (days)", self.deadline, 2)

        tk.Checkbutton(
            task_box, text="Strict Deadline",
            variable=self.strict, bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_TEXT
        ).grid(row=3, column=1, sticky="w")

        tk.Label(
            task_box, text="Task length (choose any one)",
            bg=PANEL_BLUE, fg=TEXT_COLOR, font=("Refuel", 9, "bold")
        ).grid(row=4, column=0, columnspan=2, sticky="w")

        tk.Radiobutton(
            task_box, text="Hours needed",
            variable=self.length_mode, value="hours",
            command=self.toggle_length_inputs,
            bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_TEXT
        ).grid(row=5, column=0, sticky="w")

        self.hours_entry = tk.Entry(task_box, textvariable=self.hours, width=28)
        self.hours_entry.grid(row=5, column=1)

        tk.Radiobutton(
            task_box, text="Length description",
            variable=self.length_mode, value="desc",
            command=self.toggle_length_inputs,
            bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_TEXT
        ).grid(row=6, column=0, sticky="w")

        self.length_combo = ttk.Combobox(
            task_box,
            textvariable=self.length,
            values=["Very Short", "Short", "Medium", "Long"],
            width=25,
            state="disabled"
        )
        self.length_combo.grid(row=6, column=1)

        self._combo(
            task_box,
            "Task Type (optional)",
            self.task_type,
            ["Study", "Assignment", "Revision", "Reading", "Practice"],
            7
        )

        tk.Button(
            task_box, text="Add Task",
            command=self.add_task, width=16
        ).grid(row=8, column=1, pady=4, sticky="e")

        # -------- TASK TABLE -------- #
        cols = ("Name", "Priority", "Deadline", "Strict", "Length", "Type")
        self.task_table = ttk.Treeview(
            task_box, columns=cols, show="headings", height=4
        )
        for c in cols:
            self.task_table.heading(c, text=c)
            self.task_table.column(c, width=95)
        self.task_table.grid(row=9, column=0, columnspan=2, pady=4)

        # -------- AVAILABILITY -------- #
        avail_box = tk.LabelFrame(
            self.input_panel, text="Availability & Limits",
            bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_TEXT
        )
        avail_box.pack(fill="x", padx=8, pady=6)

        self.energy = tk.StringVar(value="Normal")
        self.work_until = tk.StringVar(value="8")

        self._combo(avail_box, "Energy Level", self.energy,
                    ["Tired", "Normal", "Energetic"], 0)
        self._combo(avail_box, "Can Work For (hours)", self.work_until,
                    [str(i) for i in range(1, 9)], 1)

        self.generate_btn = tk.Button(
            self.input_panel,
            text="Generate Schedule",
            font=FONT_TEXT,
            width=20,
            command=self.generate_schedule
        )
        self.generate_btn.pack(pady=10)

        self.toggle_length_inputs()

    # ---------------- OUTPUT PANEL ---------------- #

    def build_output_panel(self, parent):
        self.output_panel = tk.Frame(parent, bg=PANEL_BLUE)
        self.output_panel.pack(side="right", fill="both", expand=True, padx=8)

        tk.Label(
            self.output_panel, text="OUTPUT",
            bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_HEADER
        ).pack(pady=3)

        self.output_table = ttk.Treeview(
            self.output_panel, columns=("Output",), show="headings"
        )
        self.output_table.heading("Output", text="Planner Output")
        self.output_table.column("Output", width=520)
        self.output_table.pack(fill="both", expand=True, padx=8, pady=8)

    # ---------------- HELPERS ---------------- #

    def _row(self, parent, label, var, row):
        tk.Label(parent, text=label,
                 bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_TEXT
                 ).grid(row=row, column=0, sticky="w")
        tk.Entry(parent, textvariable=var, width=28
                 ).grid(row=row, column=1)

    def _combo(self, parent, label, var, values, row):
        tk.Label(parent, text=label,
                 bg=PANEL_BLUE, fg=TEXT_COLOR, font=FONT_TEXT
                 ).grid(row=row, column=0, sticky="w")
        ttk.Combobox(parent, textvariable=var,
                     values=values, width=25
                     ).grid(row=row, column=1)

    def toggle_length_inputs(self):
        if self.length_mode.get() == "hours":
            self.hours_entry.config(state="normal")
            self.length_combo.config(state="disabled")
            self.length.set("")   # 🔴 ensure None is passed
        else:
            self.hours_entry.config(state="disabled")
            self.length_combo.config(state="readonly")
            self.hours.set("")

    # ---------------- LOGIC ---------------- #

    def add_task(self):
        # --- GUI validation ---
        if not self.task_name.get().strip():
            return
        if not self.deadline.get().strip():
            return

        try:
            deadline_days = int(self.deadline.get())
        except ValueError:
            return

        approx_hours = (
            float(self.hours.get())
            if self.length_mode.get() == "hours" and self.hours.get()
            else None
        )

        desc_length = (
            self.length.get()
            if self.length_mode.get() == "desc" and self.length.get()
            else None
        )

        task = TaskInput(
            name=self.task_name.get(),
            priority=self.priority.get(),
            deadline_days=deadline_days,
            strict_deadline=self.strict.get(),
            approximate_hours=approx_hours,
            descriptive_length=desc_length
        )

        self.tasks.append(task)

        length_display = f"{approx_hours}h" if approx_hours else desc_length
        self.task_table.insert(
            "", "end",
            values=(
                self.task_name.get(),
                self.priority.get(),
                deadline_days,
                "Yes" if self.strict.get() else "No",
                length_display,
                self.task_type.get()
            )
        )

        self.task_name.set("")
        self.deadline.set("")
        self.hours.set("")
        self.length.set("")
        self.strict.set(False)

    def generate_schedule(self):
        availability = AvailabilityInput(
            energy_level=self.energy.get(),
            work_until=int(self.work_until.get()),  # 🔴 FIX HERE
            blocked_days=[]
            )


        result = run_planner(UserInput(self.tasks, availability))

        self.output_table.delete(*self.output_table.get_children())
        for line in result.splitlines():
            self.output_table.insert("", "end", values=(line,))


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    TaskPlannerGUI(root)
    root.mainloop()