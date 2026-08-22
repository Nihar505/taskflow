# TaskFlow

TaskFlow is a simple command-line task and habit tracker built in Python.

> **Status:** Under Active Development 🚧  
> Task adding, completion, deletion, listing, and **due dates** are now available.

## Overview

TaskFlow is designed to help users track daily tasks and habits efficiently right from the terminal.

### Supported Features
- ➕ **Add Tasks:** Add new tasks via command line or interactive prompt with local JSON persistence.
- 📅 **Due Dates:** Optionally assign a due date in `YYYY-MM-DD` format when adding a task.
- 📋 **List Tasks:** View all tasks in a tabular format, including their due dates and status.
- ✅ **Complete Tasks:** Mark tasks as completed by ID.
- 🗑️ **Delete Tasks:** Remove tasks by ID.

### Planned Features
- 📊 View basic stats and progress

## Getting Started

### Prerequisites
- Python 3.6+

### Usage

#### Display Help
```bash
python3 main.py help
```

---

#### Adding a Task

Pass the task title directly on the command line:

```bash
python3 main.py add "Buy groceries"
```

Output:
```text
Task added successfully! (ID: 1) - 'Buy groceries'
```

Add a task **with a due date** using `--due`:

```bash
python3 main.py add "Submit quarterly report" --due 2026-09-30
```

Output:
```text
Task added successfully! (ID: 2) - 'Submit quarterly report' (due: 2026-09-30)
```

Run `add` without arguments to be prompted interactively (due date is also optional in interactive mode):

```bash
python3 main.py add
# Enter task title: Buy groceries
# Enter due date (YYYY-MM-DD) or press Enter to skip: 2026-08-31
```

**Invalid date example:**

```bash
python3 main.py add "Bad date task" --due 2026-13-99
```

Output:
```text
Error: Invalid date '2026-13-99'. Expected format: YYYY-MM-DD (e.g. 2026-09-30).
```

---

#### Listing Tasks

```bash
python3 main.py list
```

Output:
```text
ID    Status       Due Date       Title
------------------------------------------------------------
1     [ ]          -              Buy groceries
2     [ ]          2026-09-30     Submit quarterly report
3     [done]       2026-08-25     Review pull requests
```

Tasks without a due date show `-` in the Due Date column.

---

#### Completing a Task

```bash
python3 main.py complete 2
```

Output:
```text
Task 2 ('Submit quarterly report') marked as completed!
```

Run without arguments to be prompted interactively:

```bash
python3 main.py complete
```

---

#### Deleting a Task

```bash
python3 main.py delete 1
```

Output:
```text
Task 1 ('Buy groceries') deleted successfully!
```

Run without arguments to be prompted interactively:

```bash
python3 main.py delete
```

---

### Data Storage

Tasks are saved locally in `tasks.json` with unique auto-incrementing IDs, completion status, and an optional `due_date` field (`null` if not set).

Example `tasks.json`:

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "completed": false,
    "due_date": null
  },
  {
    "id": 2,
    "title": "Submit quarterly report",
    "completed": false,
    "due_date": "2026-09-30"
  }
]
```
