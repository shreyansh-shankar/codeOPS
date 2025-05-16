import os
import time
from rich.console import Console
import pyfiglet
import readchar

console = Console()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def dramatic_print(text, delay=0.01, style=None):
    if style:
        for char in text:
            console.print(char, style=style, end="", soft_wrap=True)
            time.sleep(delay)
        console.print()
    else:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

def print_banner(text="Mission Control", font="standard"):
    banner = pyfiglet.figlet_format(text, font=font)
    console.print(f"[bold cyan]{banner}[/bold cyan]")

def print_menu(options, highlight_index):
    for i, option in enumerate(options):
        if i == highlight_index:
            console.print(f"> {option}", style="reverse bold white")
        else:
            console.print(f"  {option}", style="bold cyan")

def interactive_menu(options, message=None):
    current_index = 0

    while True:
        clear_screen()
        print_banner()
        if message:
            console.print(f"{message}", style="bold cyan")
        print_menu(options, current_index)

        key = readchar.readkey()
        if key == readchar.key.UP:
            current_index = (current_index - 1) % len(options)
        elif key == readchar.key.DOWN:
            current_index = (current_index + 1) % len(options)
        elif key == readchar.key.ENTER:
            return current_index
        elif key == 'q':
            return len(options) - 1
        
def confirmation_dialog(message):
    options = ["Yes", "No"]
    index = 1

    while True:
        clear_screen()
        print_banner()
        print_menu(options, index)

        key = readchar.readkey()
        if key == readchar.key.LEFT or key == readchar.key.UP:
            index = (index - 1) % len(options)
        elif key == readchar.key.RIGHT or key == readchar.key.DOWN:
            index = (index + 1) % len(options)
        elif key == readchar.key.ENTER:
            return index == 0  # True if Yes
        elif key in ['y', 'Y']:
            return True
        elif key in ['n', 'N']:
            return False

def status_menu():
    while True:
        options = ["Deployed", "Initiated", "In Progress", "Accomplished", "Aborted", "Back"]
        choice = interactive_menu(options)

        if choice == len(options) - 1:
            return None
        else:
            return options[choice]