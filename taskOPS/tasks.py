import uuid
import json
import os
from datetime import datetime
from helper import *
from paths import setup_task_file

module_status_color = {
    "Deployed": "bold white",
    "Initiated": "bold blue",
    "In Progress": "bold yellow",
    "Accomplished" : "bold green",
    "Aborted": "bold red"}

class Task:
    LEVEL_NAMES = ["Objective", "Mission", "Operation", "Campaign"]
    MAX_LEVEL = 3  # Index-based: Campaign = level 3
    STATUS_OPTIONS = ["Deployed", "Initiated", "In Progress", "Accomplished", "Aborted"]

    def __init__(self, name, parent=None, codename=None, status="Deployed", level=0, uptime=None, register=True):
        self.name = name
        self.status = status
        self.level = level
        self.subtasks = []
        self.parent = parent
        self.uptime = uptime or datetime.fromisoformat(datetime.now().isoformat()).strftime("%Y-%m-%d %H:%M:%S")
        self.codename = codename or self._generate_codename()

        if not self.parent and register:
            manager.top_level_tasks.append(self)
    
    def _generate_codename(self):
        while True:
            codename = f"{uuid.uuid4().hex[:6].upper()}"
            if manager.is_codename_unique(codename):
                manager.used_codenames.append(codename)
                return codename
    
    def get_level_name(self):
        return Task.LEVEL_NAMES[self.level]

    def add_subtask(self, subtask_name):
        if self.can_add_subtask():
            subtask = Task(subtask_name, codename = None, parent = self)
            self.subtasks.append(subtask)
            
            curr_task = subtask
            while curr_task.parent:
                if curr_task.level >= curr_task.parent.level:
                    curr_task.parent.level += 1
                curr_task = curr_task.parent
            return subtask
        else:
            print(f"Cannot add subtask to {self.name}, max hierarchy level reached.")
            return None

    def can_add_subtask(self, level_index = 1):
        level_index = 0
        current = self
        while current.parent:
            level_index += 1
            current = current.parent
        return level_index < 3

    def print_tree(self, indent=0):
        result = f"{'    ' * indent}[{self.get_level_name()}] <{self.codename}>: {self.name} — {self.status} ({self.uptime})"
        console.print(result, style=module_status_color[self.status])
        for subtask in self.subtasks:
            subtask.print_tree(indent + 1)
    
    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "level": self.level,
            "codename": self.codename,
            "uptime": self.uptime,
            "subtasks": [t.to_dict() for t in self.subtasks]
        }
    
    @classmethod
    def from_dict(cls, data, parent=None):
        task = cls(
            name=data["name"],
            status=data["status"],
            level=data["level"],
            codename=data["codename"],
            uptime=data["uptime"],
            parent=parent,
            register=False
        )
        task.subtasks = [cls.from_dict(sub, parent=task) for sub in data.get("subtasks", [])]

        if parent is None:
            manager.top_level_tasks.append(task)

        return task

class TaskManager:
    def __init__(self, task_file):
        self.top_level_tasks = []
        self.used_codenames = []
        self.task_file = task_file

    def is_codename_unique(self, codename=None):
        return codename not in self.used_codenames

    def save_data(self, filename=None):
        filename = self.task_file
        data = [task.to_dict() for task in self.top_level_tasks]
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename=None):
        filename = self.task_file
        if not os.path.exists(filename):
            print(f"📂 {filename} not found.")
            return

        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Failed to parse {filename}.")
                return

        self.top_level_tasks = []
        self.used_codenames = []

        for task_dict in data:
            task = Task.from_dict(task_dict)

            def collect_codenames(t):
                self.used_codenames.append(t.codename)
                for sub in t.subtasks:
                    collect_codenames(sub)
            collect_codenames(task)

def retrive_active(indent=0):
    for module in manager.top_level_tasks:
        result = f"{'    ' * indent}[{module.get_level_name()}] <{module.codename}>: {module.name} — {module.status} ({module.uptime})"
        console.print("\n" + result, style=module_status_color[module.status])
        for subtask in module.subtasks:
            subtask.print_tree(indent + 1)
   
    console.print("\nPress enter to continue...", end="", style="bold cyan")

def change_module_status(task=None):
    
    while True:
        clear_screen()
        print_banner()

        # Get context
        if task:
            title = f"Inside: {task.name}"
            children = task.subtasks
        else:
            title = "Top-Level Modules"
            children = manager.top_level_tasks
        
        # Build menu options
        options=[]
        if task:
            options.append("Change Current Module Status")
        for child in children:
            options.append(f"{child.name}")
        options.append("Back")

        # Display menu
        choice = interactive_menu(options, message=f"\n=== {title} ===\n")

        # Handle selection
        if task and choice == 0:
            curr_status = status_menu() 
            if curr_status is not None:
                task.status = curr_status
                task.uptime = datetime.fromisoformat(datetime.now().isoformat()).strftime("%Y-%m-%d %H:%M:%S")
                dramatic_print(f"\n✅ Module Status updated to '{curr_status}'!\n", style="green")
                time.sleep(1.5)

        elif choice == len(options) - 1:
            # Go back
            break

        else:
            # Enter selected task
            selected_task = children[choice - 1] if task else children[choice]
            change_module_status(selected_task)

filepath = setup_task_file()
manager = TaskManager(filepath)