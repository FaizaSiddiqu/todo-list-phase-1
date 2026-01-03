# Todo Console Application

A simple yet powerful command-line todo list manager built with Python. Part of the **Hackathon II: Evolution of Todo** project.

## Features

- **Add Task** - Create tasks with title and optional description
- **View Tasks** - List all tasks with status indicators
- **Update Task** - Modify task title and description
- **Delete Task** - Remove tasks permanently
- **Mark Complete** - Toggle task completion status

## Quick Start

### Prerequisites

- Python 3.13 or higher
- UV package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/FaizaSiddiqu/todo-list-phase-1.git
   cd todo-console
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run todo
   ```

### Alternative: Direct Python Execution

```bash
uv run python -m src.cli
```

## Usage

When you run the application, you'll see a menu:

```
========================================
          TODO LIST MANAGER
========================================
Total: 0 | Done: 0 | Pending: 0

[1] Add Task
[2] View Tasks
[3] Update Task
[4] Delete Task
[5] Mark Complete
[0] Exit

Choose an option:
```

### Adding a Task

1. Select option `1`
2. Enter a title (required, max 200 characters)
3. Enter a description (optional, max 1000 characters)

### Viewing Tasks

Select option `2` to see all tasks:

```
======================================
            ALL TASKS
======================================

  #1: Buy groceries
     Milk, eggs, bread
     Created: 2026-01-03 10:00

  #2: Call mom
     Created: 2026-01-03 09:00

======================================
```

### Updating a Task

1. Select option `3`
2. Enter the task ID to update
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

### Deleting a Task

1. Select option `4`
2. Enter the task ID to delete
3. Confirm deletion

### Marking Complete

1. Select option `5`
2. Enter the task ID to toggle completion

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_operations.py

# Run with verbose output
uv run pytest -v
```

### Coverage Report

```bash
uv run pytest --cov=src --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the detailed coverage report.

## Project Structure

```
todo-console/
├── pyproject.toml          # Project configuration
├── README.md               # This file
├── .gitignore             # Git ignore rules
├── src/
│   ├── __init__.py        # Package marker
│   ├── models.py          # Task dataclass
│   ├── storage.py         # In-memory storage
│   ├── operations.py      # Business logic
│   └── cli.py             # Command-line interface
├── tests/
│   ├── __init__.py        # Test package marker
│   ├── conftest.py        # Pytest fixtures
│   ├── test_models.py     # Model tests
│   ├── test_storage.py    # Storage tests
│   └── test_operations.py # Operations tests
└── specs/
    └── 001-console-app/
        ├── spec.md        # Feature specification
        ├── plan.md        # Technical plan
        └── tasks.md       # Implementation tasks
```

## Architecture

The application follows a layered architecture:

- **CLI Layer** (cli.py) - User Interface
- **Operations Layer** (operations.py) - Business Logic
- **Storage Layer** (storage.py) - Data Access
- **Model Layer** (models.py) - Data Structures

## Design Decisions

1. **Dataclasses** - Used for clean, type-safe data structures
2. **In-Memory Storage** - Simple dict-based storage for Phase 1
3. **Validation** - All inputs validated at the operations layer
4. **Type Hints** - Full type annotations throughout
5. **No External Dependencies** - Only Python standard library for core functionality

## Validation Rules

| Field       | Min Length | Max Length | Required |
|-------------|------------|------------|----------|
| Title       | 1          | 200        | Yes      |
| Description | 0          | 1000       | No       |

## Hackathon Context

This is **Phase 1** of the Evolution of Todo hackathon:

- **Points**: 100
- **Level**: Basic
- **Deadline**: December 7, 2025
- **Goal**: Implement a functional console todo app using spec-driven development

## License

MIT License - Part of PIAIC AI-201 Hackathon II

---

Built with Python and Spec-Driven Development
