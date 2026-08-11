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
    print("  list        (Coming soon) List all tasks")
    print("  complete    (Coming soon) Mark a task as completed")
    print("  delete      (Coming soon) Delete a task")
    print("  stats       (Coming soon) View basic statistics")
    print()


def main():
    print_welcome()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ("--help", "-h", "help"):
            print_help()
        elif command == "add":
            title = " ".join(sys.argv[2:]).strip() if len(sys.argv) > 2 else None
            add_task(title)
        else:
            print(f"Command '{sys.argv[1]}' is not recognized.")
            print()
            print_help()
    else:
        print_help()


if __name__ == "__main__":
    main()
