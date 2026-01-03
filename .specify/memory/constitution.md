# Todo Console App - Project Constitution

> **Version**: 1.0.0  
> **Phase**: I - In-Memory Python Console App  
> **Created**: January 3, 2026  

## Purpose

This document establishes the non-negotiable principles, constraints, and standards for the Todo Console Application. All development decisions must align with this constitution.

---

## Core Principles

### 1. Code Quality Standards

- **Type Hints**: All functions MUST have complete type annotations
- **Docstrings**: All public functions MUST have docstrings with description, args, returns, and raises
- **Naming**: Use snake_case for functions/variables, PascalCase for classes
- **Line Length**: Maximum 88 characters (Black formatter default)
- **Imports**: Standard library first, then third-party, then local (isort order)

### 2. Data Models

- **Primary Model**: Use `@dataclass` for the `Task` model
- **Fields**: 
  - `id`: Auto-increment integer (starts at 1)
  - `title`: Required string (1-200 characters)
  - `description`: Optional string (max 1000 characters)
  - `completed`: Boolean (default: False)
  - `created_at`: datetime (auto-set on creation)
  - `updated_at`: datetime (auto-updated on modification)
- **Immutability**: Task IDs are immutable once created
- **Validation**: Validate all inputs before storing

### 3. Storage Architecture

- **In-Memory Only**: Use Python list or dict for storage
- **No Persistence**: Data is lost when application exits (by design)
- **No External Dependencies**: Pure Python standard library only
- **Thread Safety**: Not required for Phase 1 (single-threaded CLI)

### 4. Error Handling

- **Exceptions**: Raise `ValueError` for validation errors
- **Custom Errors**: Use descriptive error messages
- **Graceful Degradation**: CLI should never crash unexpectedly
- **User Feedback**: Always provide clear feedback for actions

### 5. Separation of Concerns

```
src/
├── models.py      # Data models (Task dataclass)
├── storage.py     # In-memory storage (TaskStorage class)
├── operations.py  # Business logic (CRUD operations)
└── cli.py         # User interface (CLI menu)
```

- **models.py**: Pure data structures, no logic
- **storage.py**: Only storage concerns, no business logic
- **operations.py**: Business rules and validation
- **cli.py**: Input/output only, delegates to operations

### 6. Testing Requirements

- **Test Coverage**: Minimum 80% coverage
- **Test Location**: All tests in `tests/` directory
- **Test Naming**: `test_<function_name>_<scenario>`
- **Assertions**: One primary assertion per test
- **Independence**: Tests must not depend on each other

---

## Technology Constraints

### Required Stack
- Python 3.13+
- UV for package management (development)
- Pytest for testing
- No external runtime dependencies

### Forbidden
- File I/O for persistence
- Database connections
- Network calls
- Third-party libraries in production code

---

## Feature Requirements (Basic Level)

### 1. Add Task
- Accept title (required) and description (optional)
- Auto-generate unique ID
- Set created_at to current timestamp
- Validate title length (1-200 chars)
- Validate description length (max 1000 chars)
- Return created task

### 2. List Tasks
- Display all tasks in formatted output
- Show: ID, Title, Status (✓ or ○)
- Handle empty list gracefully
- Sort by ID (ascending)

### 3. Update Task
- Find task by ID
- Update title and/or description
- Update `updated_at` timestamp
- Validate new values
- Raise error if task not found

### 4. Delete Task
- Find task by ID
- Remove from storage
- Raise error if task not found
- Return deleted task info

### 5. Mark Complete/Incomplete
- Find task by ID
- Toggle `completed` status
- Update `updated_at` timestamp
- Return updated task

---

## CLI Interface Standards

### Menu Format
```
╔════════════════════════════════════╗
║       📝 TODO CONSOLE APP          ║
╠════════════════════════════════════╣
║  1. Add Task                       ║
║  2. List Tasks                     ║
║  3. Update Task                    ║
║  4. Delete Task                    ║
║  5. Mark Complete/Incomplete       ║
║  6. Exit                           ║
╚════════════════════════════════════╝
```

### Input Prompts
- Clear, specific prompts
- Show validation requirements
- Confirm destructive actions

### Output Format
- Use emojis for visual clarity: ✅ ❌ 📝 🗑️
- Format task display consistently
- Show success/error messages clearly

---

## Spec-Driven Development Rules

1. **No Manual Coding**: All code generated via AI assistant following specs
2. **Spec First**: Write specification before implementation
3. **Iterate on Spec**: If code is wrong, fix the spec and regenerate
4. **Document Decisions**: Use ADRs for significant choices
5. **Track History**: All prompts saved in history/prompts/

---

## Non-Negotiables

1. ❌ Never store data in files
2. ❌ Never use global mutable state (except storage singleton)
3. ❌ Never expose internal implementation details in CLI
4. ✅ Always validate user input
5. ✅ Always provide user feedback
6. ✅ Always handle errors gracefully
7. ✅ Always use type hints
8. ✅ Always write tests first (TDD when possible)

---

## Success Criteria

Phase 1 is complete when:
- [ ] All 5 basic features work correctly
- [ ] All tests pass with 80%+ coverage
- [ ] Code follows all constitution principles
- [ ] README.md has setup and usage instructions
- [ ] Specs and constitution are committed
- [ ] Demo video shows all features working
