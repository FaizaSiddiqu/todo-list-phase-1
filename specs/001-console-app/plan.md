# Technical Plan: Todo Console Application

> **Feature ID**: 001-console-app  
> **Phase**: I - In-Memory Console App  
> **Created**: January 3, 2026  
> **Status**: Approved  

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                             │
│                       (cli.py)                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  main() → Menu Loop → User Input → Display Output   │    │
│  └─────────────────────────┬───────────────────────────┘    │
└────────────────────────────┼────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Operations Layer                          │
│                    (operations.py)                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  TodoOperations class                                │    │
│  │  - add_task()                                        │    │
│  │  - list_tasks()                                      │    │
│  │  - update_task()                                     │    │
│  │  - delete_task()                                     │    │
│  │  - toggle_complete()                                 │    │
│  │  - get_task()                                        │    │
│  └─────────────────────────┬───────────────────────────┘    │
└────────────────────────────┼────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     Storage Layer                            │
│                     (storage.py)                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  TaskStorage class (Singleton-like)                  │    │
│  │  - _tasks: dict[int, Task]                           │    │
│  │  - _next_id: int                                     │    │
│  │  - add(), get(), update(), delete(), list_all()      │    │
│  └─────────────────────────┬───────────────────────────┘    │
└────────────────────────────┼────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      Model Layer                             │
│                      (models.py)                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  @dataclass Task                                     │    │
│  │  - id, title, description, completed                 │    │
│  │  - created_at, updated_at                            │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Design

### 1. models.py - Data Models

**Purpose**: Define pure data structures with no business logic.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

**Design Decisions**:
- Use `@dataclass` for automatic `__init__`, `__repr__`, `__eq__`
- Use `field(default_factory=...)` for mutable defaults
- `description` is `str | None` to explicitly allow None
- Timestamps use `datetime` for precision

### 2. storage.py - Storage Layer

**Purpose**: Manage in-memory data storage with CRUD primitives.

```python
class TaskStorage:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    def add(self, task: Task) -> Task: ...
    def get(self, task_id: int) -> Task | None: ...
    def update(self, task: Task) -> Task: ...
    def delete(self, task_id: int) -> Task | None: ...
    def list_all(self) -> list[Task]: ...
    def clear(self) -> None: ...  # For testing
```

**Design Decisions**:
- Use `dict[int, Task]` for O(1) lookup by ID
- Track `_next_id` for auto-increment
- Return `Task | None` for get/delete to handle missing
- Provide `clear()` method for test isolation

### 3. operations.py - Business Logic

**Purpose**: Implement business rules, validation, and high-level operations.

```python
class TodoOperations:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
    
    def add_task(self, title: str, description: str | None = None) -> Task:
        # Validate title (1-200 chars)
        # Validate description (max 1000 chars)
        # Create Task with auto-ID
        # Store and return
    
    def list_tasks(self) -> list[Task]:
        # Return all tasks sorted by ID
    
    def get_task(self, task_id: int) -> Task:
        # Get task or raise ValueError
    
    def update_task(self, task_id: int, 
                    title: str | None = None,
                    description: str | None = None) -> Task:
        # Find task or raise ValueError
        # Update fields if provided
        # Update timestamp
        # Return updated task
    
    def delete_task(self, task_id: int) -> Task:
        # Find task or raise ValueError
        # Delete and return
    
    def toggle_complete(self, task_id: int) -> Task:
        # Find task or raise ValueError
        # Toggle completed status
        # Update timestamp
        # Return updated task
```

**Design Decisions**:
- Accept `TaskStorage` via constructor (dependency injection)
- Raise `ValueError` with descriptive messages for errors
- Return modified objects for chaining and feedback
- Validation happens in this layer, not storage

### 4. cli.py - User Interface

**Purpose**: Handle all user interaction, display, and input.

```python
def display_menu() -> None: ...
def get_user_choice() -> int: ...
def display_task(task: Task) -> None: ...
def display_task_list(tasks: list[Task]) -> None: ...
def handle_add_task(ops: TodoOperations) -> None: ...
def handle_list_tasks(ops: TodoOperations) -> None: ...
def handle_update_task(ops: TodoOperations) -> None: ...
def handle_delete_task(ops: TodoOperations) -> None: ...
def handle_toggle_complete(ops: TodoOperations) -> None: ...
def main() -> None: ...
```

**Design Decisions**:
- Separate display functions from handlers
- Each handler manages its own input/output
- `main()` runs the menu loop
- Catch exceptions and display user-friendly errors

---

## Validation Rules

### Title Validation
```python
def validate_title(title: str) -> str:
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")
    return title
```

### Description Validation
```python
def validate_description(description: str | None) -> str | None:
    if description is None:
        return None
    description = description.strip()
    if not description:
        return None
    if len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less")
    return description
```

---

## Error Handling Strategy

| Layer | Error Handling |
|-------|----------------|
| **models.py** | No error handling (pure data) |
| **storage.py** | Return None for missing items |
| **operations.py** | Raise ValueError with message |
| **cli.py** | Catch ValueError, display message, continue |

---

## File Structure

```
todo-console/
├── pyproject.toml              # Project configuration
├── README.md                   # Setup and usage guide
├── .gitignore                  # Git ignore rules
├── .specify/
│   └── memory/
│       └── constitution.md     # Project principles
├── specs/
│   └── 001-console-app/
│       ├── spec.md             # Feature specification
│       ├── plan.md             # This file
│       └── tasks.md            # Implementation tasks
├── history/
│   ├── prompts/                # Prompt history records
│   └── adr/                    # Architecture decisions
├── src/
│   ├── __init__.py             # Package marker
│   ├── models.py               # Task dataclass
│   ├── storage.py              # In-memory storage
│   ├── operations.py           # Business logic
│   └── cli.py                  # Console interface
└── tests/
    ├── __init__.py             # Package marker
    ├── test_models.py          # Model tests
    ├── test_storage.py         # Storage tests
    ├── test_operations.py      # Operations tests
    └── conftest.py             # Pytest fixtures
```

---

## Dependencies

### Runtime Dependencies
- Python 3.13+ (standard library only)

### Development Dependencies
- pytest >= 7.4.0 (testing)
- pytest-cov >= 4.1.0 (coverage)

---

## Testing Strategy

### Unit Tests

| Module | Test Focus |
|--------|------------|
| models.py | Dataclass creation, defaults |
| storage.py | CRUD operations, edge cases |
| operations.py | Validation, business rules |
| cli.py | Input parsing (mock I/O) |

### Test Fixtures (conftest.py)
```python
@pytest.fixture
def storage():
    return TaskStorage()

@pytest.fixture
def operations(storage):
    return TodoOperations(storage)

@pytest.fixture
def sample_task(operations):
    return operations.add_task("Test task", "Test description")
```

---

## Implementation Order

1. **models.py** - No dependencies
2. **storage.py** - Depends on models
3. **operations.py** - Depends on storage, models
4. **cli.py** - Depends on operations
5. **tests/** - Test each layer

---

## Quick Start (After Implementation)

```bash
# Install dependencies (development)
uv sync --dev

# Run the application
uv run python -m src.cli
# or
uv run todo

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing
```

---

## ADR: Storage Choice

**Decision**: Use `dict[int, Task]` instead of `list[Task]`

**Context**: Need to store tasks with unique IDs and support CRUD operations.

**Options**:
1. `list[Task]` - Simple, but O(n) lookup by ID
2. `dict[int, Task]` - O(1) lookup by ID, slightly more complex

**Decision**: Use dict for O(1) performance on get/update/delete.

**Consequences**: 
- Need to maintain `_next_id` counter separately
- `list_all()` returns `list(self._tasks.values())`
- Sorting done in operations layer, not storage
