import json
import os
import sys

TASKS_FILE = "tasks.json"


def load_tasks(filepath=TASKS_FILE):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks, filepath=TASKS_FILE):
    with open(filepath, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title=None):
    if not title:
        title = input("Enter task title: ").strip()

    if not title:
        print("Error: Task title cannot be empty.")
        return

    tasks = load_tasks()
    next_id = max([t.get("id", 0) for t in tasks], default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully! (ID: {next_id}) - '{title}'")


def print_welcome():
    print("==========================================")
    print("         Welcome to TaskFlow!             ")
    print("   Command-Line Task & Habit Tracker      ")
    print("==========================================")
    print()


def print_help():
    print("Usage: python main.py [command] [arguments]")
    print()
    print("Available Commands:")
    print("  help        Display this help message")
    print("  add         Add a new task (e.g. python main.py add \"Buy groceries\")")
    print("  complete    Mark a task as completed (e.g. python main.py complete 1)")
    print("  delete      Delete a task (e.g. python main.py delete 1)")
    print("  list        (Coming soon) List all tasks")
    print("  stats       (Coming soon) View basic statistics")
    print()


def complete_task(task_id_str=None):
    if not task_id_str:
        task_id_str = input("Enter task ID to mark as completed: ").strip()

    if not task_id_str:
        print("Error: Task ID is required.")
        return

    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"Error: Invalid task ID '{task_id_str}'. Task ID must be an integer.")
        return

    tasks = load_tasks()
    found_task = None
    for task in tasks:
        if task.get("id") == task_id:
            found_task = task
            break

    if not found_task:
        print(f"Error: Task with ID {task_id} was not found.")
        return

    if found_task.get("completed"):
        print(f"Task {task_id} ('{found_task.get('title')}') is already marked as completed.")
        return

    found_task["completed"] = True
    save_tasks(tasks)
    print(f"Task {task_id} ('{found_task.get('title')}') marked as completed!")


def delete_task(task_id_str=None):
    if not task_id_str:
        task_id_str = input("Enter task ID to delete: ").strip()

    if not task_id_str:
        print("Error: Task ID is required.")
        return

    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"Error: Invalid task ID '{task_id_str}'. Task ID must be an integer.")
        return

    tasks = load_tasks()
    found_task = None
    for task in tasks:
        if task.get("id") == task_id:
            found_task = task
            break

    if not found_task:
        print(f"Error: Task with ID {task_id} was not found.")
        return

    tasks = [t for t in tasks if t.get("id") != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} ('{found_task.get('title')}') deleted successfully!")


def main():
    print_welcome()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ("--help", "-h", "help"):
            print_help()
        elif command == "add":
            title = " ".join(sys.argv[2:]).strip() if len(sys.argv) > 2 else None
            add_task(title)
        elif command == "complete":
            task_id_arg = sys.argv[2] if len(sys.argv) > 2 else None
            complete_task(task_id_arg)
        elif command == "delete":
            task_id_arg = sys.argv[2] if len(sys.argv) > 2 else None
            delete_task(task_id_arg)
        else:
            print(f"Command '{sys.argv[1]}' is not recognized.")
            print()
            print_help()
    else:
        print_help()


if __name__ == "__main__":
    main()
