import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager
from themes import LIGHT_THEME, DARK_THEME

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.manager = TaskManager()
        self.theme = LIGHT_THEME

        self.build_ui()
        self.apply_theme()
        self.refresh_listbox()

    def build_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.task_entry = tk.Entry(self.frame, width=30)
        self.task_entry.grid(row=0, column=0, padx=5)
        self.due_entry = tk.Entry(self.frame, width=15)
        self.due_entry.insert(0, "YYYY-MM-DD")
        self.due_entry.grid(row=0, column=1, padx=5)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=5)

        self.tasks_listbox = tk.Listbox(self.root, width=60)
        self.tasks_listbox.pack(pady=10)

        self.complete_button = tk.Button(self.root, text="Toggle Complete", command=self.toggle_task)
        self.complete_button.pack(pady=2)

        self.remove_button = tk.Button(self.root, text="Remove", command=self.remove_task)
        self.remove_button.pack(pady=2)

        self.theme_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(pady=5)

    def apply_theme(self):
        theme = self.theme
        self.root.configure(bg=theme["bg"])
        self.frame.configure(bg=theme["bg"])
        for widget in self.frame.winfo_children():
            widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])

        self.task_entry.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
        self.due_entry.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])

        self.tasks_listbox.configure(bg=theme["listbox_bg"], fg=theme["listbox_fg"])
        for btn in [self.add_button, self.complete_button, self.remove_button, self.theme_button]:
            btn.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])

    def refresh_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.get_tasks():
            status = "[✔]" if task['completed'] else "[ ]"
            due = f"(Due: {task['due_date']})" if task['due_date'] else ""
            self.tasks_listbox.insert(tk.END, f"{status} {task['task']} {due}")

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_entry.get().strip()
        if due_date and due_date != "YYYY-MM-DD":
            try:
                from datetime import datetime
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Date format should be YYYY-MM-DD")
                return
        else:
            due_date = None
        self.manager.add_task(task, due_date)
        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, "YYYY-MM-DD")
        self.refresh_listbox()

    def remove_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            self.manager.remove_task(selected[0])
            self.refresh_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def toggle_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            self.manager.toggle_task(selected[0])
            self.refresh_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to toggle.")

    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        self.apply_theme()
