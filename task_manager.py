import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, task, due_date=None):
        if task.strip():
            self.tasks.append({
                'task': task.strip(),
                'completed': False,
                'due_date': due_date
            })
            self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]['completed'] = not self.tasks[index]['completed']
            self.save_tasks()

    def get_tasks(self):
        return sorted(self.tasks, key=lambda t: t['completed'])

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.tasks = json.load(f)
