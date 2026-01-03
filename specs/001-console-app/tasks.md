# Implementation Tasks: Todo Console Application

> **Feature ID**: 001-console-app  
> **Phase**: I - In-Memory Console App  
> **Created**: January 3, 2026  
> **Status**: Ready for Implementation  

---

## Task Overview

| ID | Task | Priority | Estimate | Status |
|----|------|----------|----------|--------|
| T-001 | Create Task dataclass in models.py | High | 10 min | ✅ |
| T-002 | Implement TaskStorage class | High | 20 min | ✅ |
| T-003 | Write storage unit tests | High | 15 min | ✅ |
| T-004 | Implement TodoOperations class | High | 30 min | ✅ |
| T-005 | Write operations unit tests | High | 20 min | ✅ |
| T-006 | Implement CLI display functions | Medium | 20 min | ✅ |
| T-007 | Implement CLI handlers | Medium | 30 min | ✅ |
| T-008 | Implement main menu loop | Medium | 15 min | ✅ |
| T-009 | Create README.md | Low | 15 min | ✅ |
| T-010 | Final testing and polish | Low | 15 min | ✅ |

**Total Estimated Time**: ~3 hours
**Actual Completion**: All tasks completed ✅

---

## Detailed Task Descriptions

### T-001: Create Task Dataclass
**File**: `src/models.py`

**Requirements**:
- Create `@dataclass` class named `Task`
- Fields:
  - `id: int` - Unique identifier
  - `title: str` - Task title (required)
  - `description: str | None` - Optional description (default: None)
  - `completed: bool` - Completion status (default: False)
  - `created_at: datetime` - Auto-set to now
  - `updated_at: datetime` - Auto-set to now
- Use `field(default_factory=datetime.now)` for timestamps
- Add type hints to all fields

**Acceptance Criteria**:
- [ ] Dataclass can be instantiated with just id and title
- [ ] Default values work correctly
- [ ] `__repr__` shows useful output
- [ ] Timestamps are set automatically

---

### T-002: Implement TaskStorage Class
**File**: `src/storage.py`

**Requirements**:
- Create `TaskStorage` class with:
  - `_tasks: dict[int, Task]` - Private storage
  - `_next_id: int` - Auto-increment counter (starts at 1)
- Methods:
  - `generate_id() -> int` - Get next ID and increment
  - `add(task: Task) -> Task` - Store task, return it
  - `get(task_id: int) -> Task | None` - Get by ID or None
  - `update(task: Task) -> Task` - Update existing task
  - `delete(task_id: int) -> Task | None` - Remove and return
  - `list_all() -> list[Task]` - Get all tasks as list
  - `clear() -> None` - Remove all tasks (for testing)
  - `count() -> int` - Return number of tasks

**Acceptance Criteria**:
- [ ] IDs auto-increment from 1
- [ ] Get returns None for non-existent ID
- [ ] Delete returns removed task or None
- [ ] list_all returns tasks sorted by ID
- [ ] Clear removes all tasks and resets ID counter

---

### T-003: Write Storage Unit Tests
**File**: `tests/test_storage.py`

**Test Cases**:
```python
def test_generate_id_starts_at_one(): ...
def test_generate_id_increments(): ...
def test_add_task_stores_task(): ...
def test_get_existing_task(): ...
def test_get_nonexistent_task_returns_none(): ...
def test_update_task(): ...
def test_delete_existing_task(): ...
def test_delete_nonexistent_task_returns_none(): ...
def test_list_all_empty(): ...
def test_list_all_with_tasks(): ...
def test_list_all_sorted_by_id(): ...
def test_clear_removes_all(): ...
def test_count(): ...
```

**Acceptance Criteria**:
- [ ] All tests pass
- [ ] Edge cases covered
- [ ] Tests are independent

---

### T-004: Implement TodoOperations Class
**File**: `src/operations.py`

**Requirements**:
- Create `TodoOperations` class with:
  - Constructor accepts `TaskStorage` instance
  - Stores as `self.storage`
- Methods:
  - `add_task(title: str, description: str | None = None) -> Task`
    - Validate title (strip, check 1-200 chars)
    - Validate description (strip, check max 1000 chars, None if empty)
    - Generate ID via storage
    - Create Task with current timestamps
    - Store and return
  - `list_tasks() -> list[Task]`
    - Return all tasks from storage
  - `get_task(task_id: int) -> Task`
    - Get from storage
    - Raise `ValueError` if not found
  - `update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task`
    - Get task or raise `ValueError`
    - Update title if provided (validate)
    - Update description if provided (validate)
    - Update `updated_at` timestamp
    - Store and return
  - `delete_task(task_id: int) -> Task`
    - Get task or raise `ValueError`
    - Delete from storage
    - Return deleted task
  - `toggle_complete(task_id: int) -> Task`
    - Get task or raise `ValueError`
    - Flip `completed` status
    - Update `updated_at` timestamp
    - Store and return
- Helper functions:
  - `validate_title(title: str) -> str`
  - `validate_description(description: str | None) -> str | None`

**Acceptance Criteria**:
- [ ] Validation rejects empty title
- [ ] Validation rejects title > 200 chars
- [ ] Validation rejects description > 1000 chars
- [ ] ValueError has descriptive message
- [ ] Timestamps update correctly

---

### T-005: Write Operations Unit Tests
**File**: `tests/test_operations.py`

**Test Cases**:
```python
# Add task tests
def test_add_task_valid(): ...
def test_add_task_with_description(): ...
def test_add_task_empty_title_raises(): ...
def test_add_task_whitespace_title_raises(): ...
def test_add_task_title_too_long_raises(): ...
def test_add_task_description_too_long_raises(): ...
def test_add_task_empty_description_becomes_none(): ...

# List tasks tests
def test_list_tasks_empty(): ...
def test_list_tasks_with_tasks(): ...

# Get task tests
def test_get_task_exists(): ...
def test_get_task_not_found_raises(): ...

# Update task tests
def test_update_task_title(): ...
def test_update_task_description(): ...
def test_update_task_both(): ...
def test_update_task_not_found_raises(): ...
def test_update_task_updates_timestamp(): ...

# Delete task tests
def test_delete_task_exists(): ...
def test_delete_task_not_found_raises(): ...

# Toggle complete tests
def test_toggle_complete_to_true(): ...
def test_toggle_complete_to_false(): ...
def test_toggle_complete_not_found_raises(): ...
def test_toggle_complete_updates_timestamp(): ...
```

**Acceptance Criteria**:
- [ ] All tests pass
- [ ] Both success and error paths tested
- [ ] Validation edge cases covered

---

### T-006: Implement CLI Display Functions
**File**: `src/cli.py`

**Requirements**:
- `display_menu() -> None`
  - Print formatted menu with box drawing characters
  - Show all 6 options with emojis
- `display_task(task: Task, detailed: bool = False) -> None`
  - Show task with status indicator (✓ or ○)
  - If detailed, show description and timestamps
- `display_task_list(tasks: list[Task]) -> None`
  - Show all tasks in formatted list
  - Show summary counts (total, completed, pending)
  - Handle empty list gracefully
- `display_success(message: str) -> None`
  - Print success message with ✅ emoji
- `display_error(message: str) -> None`
  - Print error message with ❌ emoji
- `get_input(prompt: str) -> str`
  - Print prompt and get input
  - Strip whitespace

**Acceptance Criteria**:
- [ ] Menu displays correctly
- [ ] Tasks show correct status indicator
- [ ] Empty list shows friendly message
- [ ] Messages use appropriate emojis

---

### T-007: Implement CLI Handlers
**File**: `src/cli.py` (continued)

**Requirements**:
- `handle_add_task(ops: TodoOperations) -> None`
  - Prompt for title (required)
  - Prompt for description (optional)
  - Call `ops.add_task()`
  - Display success or error
- `handle_list_tasks(ops: TodoOperations) -> None`
  - Get tasks from `ops.list_tasks()`
  - Display using `display_task_list()`
- `handle_update_task(ops: TodoOperations) -> None`
  - Prompt for task ID
  - Show current task details
  - Prompt for new title (Enter to keep)
  - Prompt for new description (Enter to keep)
  - Call `ops.update_task()`
  - Display success or error
- `handle_delete_task(ops: TodoOperations) -> None`
  - Prompt for task ID
  - Show task details
  - Confirm deletion (y/n)
  - Call `ops.delete_task()` if confirmed
  - Display result
- `handle_toggle_complete(ops: TodoOperations) -> None`
  - Prompt for task ID
  - Call `ops.toggle_complete()`
  - Display new status

**Acceptance Criteria**:
- [ ] All handlers catch ValueError and display error
- [ ] Invalid ID input handled gracefully
- [ ] Delete requires confirmation
- [ ] Success messages shown after operations

---

### T-008: Implement Main Menu Loop
**File**: `src/cli.py` (continued)

**Requirements**:
- `main() -> None`
  - Create `TaskStorage` instance
  - Create `TodoOperations` instance
  - Display welcome message
  - Loop:
    - Display menu
    - Get user choice
    - Call appropriate handler
    - Handle invalid choice
  - Handle Ctrl+C gracefully (exit message)
  - Handle choice 6 (Exit) with goodbye message

**Acceptance Criteria**:
- [ ] Menu loop runs until exit
- [ ] Invalid choices show error and continue
- [ ] Ctrl+C exits gracefully
- [ ] Exit shows goodbye message

---

### T-009: Create README.md
**File**: `README.md`

**Sections**:
1. **Title and Description**
   - Project name: Todo Console App
   - Phase 1 of Hackathon II
   - Brief description
2. **Features**
   - List all 5 features
3. **Requirements**
   - Python 3.13+
   - UV (optional)
4. **Installation**
   - Clone repo
   - Install dependencies
5. **Usage**
   - How to run
   - Example commands
6. **Development**
   - Run tests
   - Code structure
7. **Spec-Driven Development**
   - Link to specs
   - Methodology used

**Acceptance Criteria**:
- [ ] Clear installation instructions
- [ ] Usage examples included
- [ ] Formatted with proper Markdown

---

### T-010: Final Testing and Polish
**File**: All files

**Requirements**:
- Run full test suite with coverage
- Ensure 80%+ coverage
- Test all features manually
- Fix any bugs found
- Clean up code formatting
- Verify all specs are accurate
- Create demo video

**Acceptance Criteria**:
- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] Manual testing complete
- [ ] Demo video recorded
- [ ] Ready for submission

---

## Progress Tracking

### Implementation Log

| Date | Task | Time Spent | Notes |
|------|------|------------|-------|
| | | | |

### Blockers

| Issue | Task | Resolution |
|-------|------|------------|
| | | |

---

## Definition of Done (Per Task)

- [ ] Code written following constitution
- [ ] Type hints added
- [ ] Docstrings added
- [ ] Tests written (if applicable)
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Task marked complete
