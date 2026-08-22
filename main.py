import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"
DATE_FORMAT = "%Y-%m-%d"


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


def parse_due_date(date_str):
    """Parse a YYYY-MM-DD string and return it if valid, else raise ValueError."""
    try:
        parsed = datetime.strptime(date_str.strip(), DATE_FORMAT)
    except ValueError:
        raise ValueError(
            f"Invalid date '{date_str}'. Expected format: YYYY-MM-DD (e.g. 2026-09-30)."
        )
    # Basic sanity check: year must be reasonable
    if parsed.year < 2000 or parsed.year > 2100:
        raise ValueError(
            f"Date '{date_str}' looks unreasonable. Year must be between 2000 and 2100."
        )
    return parsed.strftime(DATE_FORMAT)


def add_task(title=None, due_date_str=None):
    if not title:
        title = input("Enter task title: ").strip()

    if not title:
        print("Error: Task title cannot be empty.")
        return

    # Handle due date
    due_date = None
    if due_date_str is None:
        # Not passed via CLI — ask interactively (optional)
        raw = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
        if raw:
            try:
                due_date = parse_due_date(raw)
            except ValueError as e:
                print(f"Error: {e}")
                return
    elif due_date_str:
        try:
            due_date = parse_due_date(due_date_str)
        except ValueError as e:
            print(f"Error: {e}")
            return

    tasks = load_tasks()
    next_id = max([t.get("id", 0) for t in tasks], default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "completed": False,
        "due_date": due_date,  # None if not provided
    }

    tasks.append(new_task)
    save_tasks(tasks)

    due_display = f" (due: {due_date})" if due_date else ""
    print(f"Task added successfully! (ID: {next_id}) - '{title}'{due_display}")


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found. Add one with: python main.py add \"Your task\"")
        return

    print(f"{'ID':<5} {'Status':<12} {'Due Date':<14} Title")
    print("-" * 60)

    for task in tasks:
        status = "[done]" if task.get("completed") else "[ ]  "
        due = task.get("due_date") or "-"
        title = task.get("title", "")
        print(f"{task.get('id'):<5} {status:<12} {due:<14} {title}")


def show_stats():
    tasks = load_tasks()
    total = len(tasks)

    if total == 0:
        print("No tasks found. Add one with: python main.py add \"Your task\"")
        return

    completed = sum(1 for t in tasks if t.get("completed"))
    incomplete = total - completed
    pct = (completed / total) * 100

    # Overdue: incomplete tasks whose due_date is before today
    today_str = datetime.now().strftime(DATE_FORMAT)
    overdue = sum(
        1 for t in tasks
        if not t.get("completed")
        and t.get("due_date")
        and t["due_date"] < today_str  # lexicographic comparison works for YYYY-MM-DD
    )

    print("--- Task Statistics ---")
    print(f"  Total tasks      : {total}")
    print(f"  Completed        : {completed}")
    print(f"  Incomplete       : {incomplete}")
    print(f"  Completion       : {pct:.1f}%")
    print(f"  Overdue          : {overdue}")


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
    print("  add         Add a new task")
    print("                python main.py add \"Buy groceries\"")
    print("                python main.py add \"Submit report\" --due 2026-09-30")
    print("  list        List all tasks")
    print("                python main.py list")
    print("  complete    Mark a task as completed (e.g. python main.py complete 1)")
    print("  delete      Delete a task (e.g. python main.py delete 1)")
    print("  stats       Show task statistics (e.g. python main.py stats)")
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
            # Parse optional --due flag anywhere after 'add'
            args = sys.argv[2:]
            due_date_str = None
            title_parts = []

            i = 0
            while i < len(args):
                if args[i] == "--due" and i + 1 < len(args):
                    due_date_str = args[i + 1]
                    i += 2
                else:
                    title_parts.append(args[i])
                    i += 1

            title = " ".join(title_parts).strip() if title_parts else None
            add_task(title, due_date_str)
        elif command == "list":
            list_tasks()
        elif command == "complete":
            task_id_arg = sys.argv[2] if len(sys.argv) > 2 else None
            complete_task(task_id_arg)
        elif command == "stats":
            show_stats()
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
