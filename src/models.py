"""
Task Model Module

Defines the Task dataclass for representing todo items.
This module contains pure data structures with no business logic.

Reference: specs/001-console-app/spec.md
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """
    Represents a todo task item.
    
    Attributes:
        id: Unique identifier for the task (auto-increment integer).
        title: The task title (required, 1-200 characters).
        description: Optional task description (max 1000 characters).
        completed: Whether the task is completed (default: False).
        created_at: Timestamp when task was created.
        updated_at: Timestamp when task was last updated.
    
    Example:
        >>> task = Task(id=1, title="Buy groceries")
        >>> task.completed
        False
        >>> task.description is None
        True
    """
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        status = "✓" if self.completed else "○"
        return f"[{status}] #{self.id}: {self.title}"
