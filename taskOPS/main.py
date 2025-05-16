import time
import sys
from tasks import *
from helper import *
from paths import setup_task_file

missions = [
    "Deploy New Modules",
    "Review Active Modules",
    "Change a Module Status",
    "Decommision a Module",
    "Stand Down (Exit)"
]

def deploy_menu(task=None):
    """
    Displays the deploy menu for either top-level or a given task.
    """
    while True:
        clear_screen()
        print_banner()

        # Get context
        if task:
            title = f"Inside: {task.name}"
            children = task.subtasks
        else:
            title = "Top-Level Deploy Menu"
            children = manager.top_level_tasks

        # Build menu options
        options = ["Deploy a new Objective"]
        for child in children:
            options.append(f"{child.name}")
        options.append("Back")

        # Display menu
        choice = interactive_menu(options, message=f"\n=== {title} ===\n")

        # Handle selection
        if choice == 0:
            # Deploy new task (under this task if exists)
            new_title = input("\nEnter the new Objective name: ").strip()
            if new_title:
                if task:
                    task.add_subtask(new_title)
                else:
                    temp = Task(name=new_title)
                dramatic_print(f"\n✅ Objective '{new_title}' deployed!\n", style="green")
                time.sleep(1.5)

        elif choice == len(options) - 1:
            # Go back
            break

        else:
            # Enter selected task
            selected_task = children[choice - 1]
            deploy_menu(selected_task)

def decommission_module(task=None):
    while True:
        clear_screen()
        print_banner()

        # Set context
        if task:
            title = f"Inside: {task.name}"
            children = task.subtasks
        else:
            title = "Top-Level Modules"
            children = manager.top_level_tasks

        # Build menu
        options=[]
        if task:
            options.append("Decommission the module")
        options.extend([f"{child.name}" for child in children])
        options.append("Back")

        choice = interactive_menu(options, message=f"\n Decommission Module — {title}")

        if task and choice == 0:
            confirm = input(f"\nAre you sure you want to decommission '{task.name}' and all its sub modules? (y/n): ").lower()
            if confirm == "y":
                if task.parent:
                    task.parent.subtasks.remove(task)
                elif task in manager.top_level_tasks:
                    manager.top_level_tasks.remove(task)
                dramatic_print(f"\n'{task.name}' has been decommissioned!\n", style="red")
                time.sleep(1)
                return
            else:
                print("Decommission aborted.")
                time.sleep(1)
                return
        elif choice == len(options) - 1:
            break
        else:
            # Enter selected task
            selected_task = children[choice - 1] if task else children[choice]
            decommission_module(selected_task)

def main():
    task_file_path = setup_task_file()
    if not task_file_path:
        print("❌ Could not set up task file. Exiting.")
        time.sleep(2.5)
        return
    boot_sequence()
    manager.load_from_file(task_file_path)
    
    while True:
        choice = interactive_menu(missions)
        
        if choice == 0:
            deploy_menu()
        
        elif choice == 1:
            clear_screen()
            print_banner()
            dramatic_print(">>> Retrieving all modules...", style="bold green")
            retrive_active()
            input()

        elif choice == 2:
            clear_screen()
            print_banner()
            dramatic_print(">>> Changing module status...", style="bold green")
            change_module_status()

        elif choice == 3:
            clear_screen()
            print_banner()
            dramatic_print(">>> Decommissioning a module...", style="bold green")
            decommission_module()

        elif choice == 4:
            clear_screen()
            print_banner()
            manager.save_data()
            dramatic_print(">>> Standing down... Mission Control terminated.", style="bold red")
            break

def boot_sequence():
    clear_screen()
    print_banner()
    dramatic_print(">>> Initializing BlackSite Command Interface...", style="bold cyan")
    time.sleep(0.5)
    dramatic_print(">>> Establishing Secure Uplink with HQ...", style="bold cyan")
    time.sleep(0.5)
    dramatic_print(">>> Loading Mission Protocols...", style="bold cyan")
    time.sleep(0.5)
    dramatic_print(">>> Commander Authorization Required...", style="bold yellow")
    input(">>> Enter Authorization Code: ************ (Press Enter to continue)\n")
    dramatic_print(">>> Access Granted. Welcome back, Commander.", style="bold green")
    dramatic_print(">>> Standing by for new operations...\n", style="bold green")
    time.sleep(1)

if __name__ == "__main__":
    main()
