# Feature Specification: Todo Console Application

> **Feature ID**: 001-console-app  
> **Phase**: I - In-Memory Console App  
> **Created**: January 3, 2026  
> **Status**: In Progress  

---

## Overview

Build a command-line todo application that allows users to manage tasks through a simple menu-driven interface. All data is stored in memory and will be lost when the application exits.

---

## User Stories

### US-001: Add Task
**As a** user  
**I want to** add a new task with a title and optional description  
**So that** I can track things I need to do

**Acceptance Criteria:**
- [ ] User is prompted for task title (required)
- [ ] User is prompted for description (optional, can press Enter to skip)
- [ ] Task is assigned a unique auto-increment ID starting from 1
- [ ] Task title must be 1-200 characters
- [ ] Task description must be 0-1000 characters
- [ ] Task is created with `completed = False`
- [ ] Task is created with current timestamp for `created_at` and `updated_at`
- [ ] Success message shows the created task details
- [ ] Error message shown if validation fails

### US-002: List Tasks
**As a** user  
**I want to** see all my tasks  
**So that** I can review what needs to be done

**Acceptance Criteria:**
- [ ] All tasks are displayed in a formatted list
- [ ] Each task shows: ID, Title, Status indicator (✓ completed, ○ pending)
- [ ] Tasks are sorted by ID in ascending order
- [ ] If no tasks exist, show friendly "No tasks yet" message
- [ ] Display total count of tasks (X total, Y completed, Z pending)

### US-003: Update Task
**As a** user  
**I want to** modify an existing task's title or description  
**So that** I can correct or improve task details

**Acceptance Criteria:**
- [ ] User is prompted for task ID
- [ ] If ID doesn't exist, show error message
- [ ] Current task details are displayed
- [ ] User can update title (press Enter to keep current)
- [ ] User can update description (press Enter to keep current)
- [ ] At least one field must change (or show "no changes" message)
- [ ] `updated_at` timestamp is updated
- [ ] Success message shows updated task details

### US-004: Delete Task
**As a** user  
**I want to** remove a task from my list  
**So that** I can clean up completed or cancelled tasks

**Acceptance Criteria:**
- [ ] User is prompted for task ID
- [ ] If ID doesn't exist, show error message
- [ ] Task details are shown with confirmation prompt
- [ ] User must type 'y' or 'yes' to confirm deletion
- [ ] Task is removed from storage
- [ ] Success message confirms deletion
- [ ] User can cancel deletion by entering anything else

### US-005: Mark Complete/Incomplete
**As a** user  
**I want to** toggle the completion status of a task  
**So that** I can track my progress

**Acceptance Criteria:**
- [ ] User is prompted for task ID
- [ ] If ID doesn't exist, show error message
- [ ] Current status is displayed
- [ ] Status is toggled (complete ↔ incomplete)
- [ ] `updated_at` timestamp is updated
- [ ] Success message shows new status

---

## Data Model

### Task Entity
```python
@dataclass
class Task:
    id: int                           # Unique identifier (auto-increment)
    title: str                        # Task title (1-200 chars)
    description: str | None           # Optional description (max 1000 chars)
    completed: bool                   # Completion status
    created_at: datetime              # Creation timestamp
    updated_at: datetime              # Last update timestamp
```

### Validation Rules
| Field | Type | Required | Min | Max | Default |
|-------|------|----------|-----|-----|---------|
| id | int | Auto | 1 | ∞ | Auto-increment |
| title | str | Yes | 1 | 200 | - |
| description | str | No | 0 | 1000 | None |
| completed | bool | No | - | - | False |
| created_at | datetime | Auto | - | - | Now |
| updated_at | datetime | Auto | - | - | Now |

---

## User Interface

### Main Menu
```
╔════════════════════════════════════════╗
║         📝 TODO CONSOLE APP            ║
╠════════════════════════════════════════╣
║  [1] ➕ Add Task                       ║
║  [2] 📋 List Tasks                     ║
║  [3] ✏️  Update Task                    ║
║  [4] 🗑️  Delete Task                    ║
║  [5] ✅ Toggle Complete                ║
║  [6] 🚪 Exit                           ║
╚════════════════════════════════════════╝

Enter your choice (1-6): _
```

### Task Display Format
```
┌─────────────────────────────────────────┐
│ #1 ○ Buy groceries                      │
│    📝 Milk, eggs, bread                 │
│    📅 Created: 2026-01-03 10:30         │
├─────────────────────────────────────────┤
│ #2 ✓ Call mom                           │
│    📅 Created: 2026-01-03 09:15         │
└─────────────────────────────────────────┘

📊 Total: 2 tasks | ✅ Completed: 1 | ⏳ Pending: 1
```

---

## Error Handling

### Error Messages
| Scenario | Message |
|----------|---------|
| Task not found | "❌ Error: Task with ID {id} not found" |
| Empty title | "❌ Error: Title cannot be empty" |
| Title too long | "❌ Error: Title must be 200 characters or less" |
| Description too long | "❌ Error: Description must be 1000 characters or less" |
| Invalid menu choice | "❌ Invalid choice. Please enter 1-6" |
| Invalid ID format | "❌ Error: Please enter a valid number" |

### Recovery
- After any error, return to main menu
- Never crash the application
- Always provide actionable feedback

---

## Non-Functional Requirements

### Performance
- All operations complete in < 100ms
- Support up to 10,000 tasks in memory

### Usability
- Clear prompts and instructions
- Consistent formatting
- Keyboard-only navigation

### Reliability
- No data corruption within session
- Graceful handling of Ctrl+C (exit message)

---

## Out of Scope (Phase 1)

- ❌ Persistent storage (files, database)
- ❌ Multiple users
- ❌ Due dates and reminders
- ❌ Priorities and tags
- ❌ Search and filter
- ❌ Recurring tasks
- ❌ Data export/import

---

## Testing Requirements

### Unit Tests Required
- [ ] Test add_task with valid input
- [ ] Test add_task with invalid title (empty, too long)
- [ ] Test add_task with invalid description (too long)
- [ ] Test list_tasks with empty storage
- [ ] Test list_tasks with multiple tasks
- [ ] Test update_task with valid changes
- [ ] Test update_task with non-existent ID
- [ ] Test delete_task with valid ID
- [ ] Test delete_task with non-existent ID
- [ ] Test toggle_complete changes status correctly

### Integration Tests
- [ ] Full workflow: add → list → update → complete → delete
- [ ] Multiple tasks lifecycle

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] All unit tests passing
- [ ] Code coverage ≥ 80%
- [ ] No linting errors
- [ ] Code reviewed against constitution
- [ ] README.md updated
- [ ] Demo video recorded
