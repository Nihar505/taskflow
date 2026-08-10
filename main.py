import sys


def print_welcome():
    print("==========================================")
    print("         Welcome to TaskFlow!             ")
    print("   Command-Line Task & Habit Tracker      ")
    print("==========================================")
    print()


def print_help():
    print("Usage: python main.py [command]")
    print()
    print("Available Commands:")
    print("  help        Display this help message")
    print("  add         (Coming soon) Add a new task or habit")
    print("  list        (Coming soon) List all tasks")
    print("  complete    (Coming soon) Mark a task as completed")
    print("  delete      (Coming soon) Delete a task")
    print("  stats       (Coming soon) View basic statistics")
    print()
    print("Note: TaskFlow is currently under development.")


def main():
    print_welcome()

    # Simple command-line argument handling
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ("--help", "-h", "help"):
            print_help()
        else:
            print(f"Command '{sys.argv[1]}' is not yet implemented.")
            print()
            print_help()
    else:
        print_help()


if __name__ == "__main__":
    main()
