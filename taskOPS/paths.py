import os
import shutil

def get_home_task_dir():
    return os.path.join(os.path.expanduser("~"), "taskOPS")

def get_user_task_file_path():
    return os.path.join(get_home_task_dir(), "tasks.json")

def setup_task_file():
    """
    Ensures that ~/taskOPS/tasks.json exists.
    If not, copies the default tasks.json from project directory to there.
    Returns the full path to the user's task file.
    """
    user_task_file = get_user_task_file_path()

    if not os.path.exists(user_task_file):
        os.makedirs(get_home_task_dir(), exist_ok=True)

        # Path to the default template inside the project
        default_template = os.path.join(os.path.dirname(__file__), "tasks.json")

        if os.path.exists(default_template):
            shutil.copy(default_template, user_task_file)
        else:
            return None

    return user_task_file
