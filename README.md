# TaskFlow

TaskFlow is a simple command-line task and habit tracker built in Python.

> **Status:** Under Active Development 🚧  
> Task adding feature with local JSON persistence is now available.

## Overview

TaskFlow is designed to help users track daily tasks and habits efficiently right from the terminal.

### Supported Features
- ➕ **Add Tasks:** Add new tasks via command line or interactive prompt with local JSON persistence.

### Planned Features
- 📋 List active tasks
- ✅ Complete tasks
- 🗑️ Delete tasks
- 📅 Assign due dates
- 📊 View basic stats and progress

## Getting Started

### Prerequisites
- Python 3.6+

### Usage

#### Display Help
```bash
python3 main.py help
```

#### Adding a Task
Pass the task title directly on the command line:

```bash
python3 main.py add "Buy groceries"
```

Output:
```text
Task added successfully! (ID: 1) - 'Buy groceries'
```

Alternatively, run `add` without title arguments to be prompted interactively:

```bash
python3 main.py add
```

### Data Storage
Tasks are automatically saved locally in `tasks.json` with unique auto-incrementing IDs and completion status.
