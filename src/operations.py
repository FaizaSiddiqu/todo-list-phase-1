"""
Todo Operations Module

Provides business logic and validation for task management.
This module implements the core functionality of the todo application.

Reference: specs/001-console-app/plan.md
"""

from datetime import datetime
from typing import List, Optional
from src.models import Task
from src.storage import TaskStorage


# Validation constants
TITLE_MIN_LENGTH = 1
TITLE_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 1000


def validate_title(title: str) -> str:
    """
    Validate and clean a task title.
    
    Args:
        title: The title string to validate.
    
    Returns:
        The cleaned (stripped) title string.
    
    Raises:
        ValueError: If title is empty or exceeds 200 characters.
    
    Example:
        >>> validate_title("  Buy groceries  ")
        'Buy groceries'
        >>> validate_title("")
        Traceback (most recent call last):
        ...
        ValueError: Title cannot be empty
    """
    title = title.strip()
    
    if not title:
        raise ValueError("Title cannot be empty")
    
    if len(title) > TITLE_MAX_LENGTH:
        raise ValueError(f"Title must be {TITLE_MAX_LENGTH} characters or less (got {len(title)})")
    
    return title


def validate_description(description: Optional[str]) -> Optional[str]:
    """
    Validate and clean a task description.
    
    Args:
        description: The description string to validate, or None.
    
    Returns:
        The cleaned description string, or None if empty.
    
    Raises:
        ValueError: If description exceeds 1000 characters.
    
    Example:
        >>> validate_description("  Some details  ")
        'Some details'
        >>> validate_description("   ") is None
        True
        >>> validate_description(None) is None
        True
    """
    if description is None:
        return None
    
    description = description.strip()
    
    if not description:
        return None
    
    if len(description) > DESCRIPTION_MAX_LENGTH:
        raise ValueError(
            f"Description must be {DESCRIPTION_MAX_LENGTH} characters or less (got {len(description)})"
        )
    
    return description


class TodoOperations:
    """
    Business logic layer for task management.
    
    Provides high-level operations with validation and error handling.
    Delegates storage to a TaskStorage instance.
    
    Attributes:
        storage: The TaskStorage instance for data persistence.
    
    Example:
        >>> from src.storage import TaskStorage
        >>> ops = TodoOperations(TaskStorage())
        >>> task = ops.add_task("Buy milk")
        >>> task.title
        'Buy milk'
    """
    
    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize with a storage instance.
        
        Args:
            storage: The TaskStorage instance to use.
        """
        self.storage = storage
    
    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create and store a new task.
        
        Args:
            title: The task title (required, 1-200 chars).
            description: Optional task description (max 1000 chars).
        
        Returns:
            The created Task object.
        
        Raises:
            ValueError: If validation fails for title or description.
        
        Example:
            >>> ops = TodoOperations(TaskStorage())
            >>> task = ops.add_task("Buy groceries", "Milk, eggs, bread")
            >>> task.id
            1
            >>> task.completed
            False
        """
        # Validate inputs
        title = validate_title(title)
        description = validate_description(description)
        
        # Generate unique ID
        task_id = self.storage.generate_id()
        
        # Create task with current timestamps
        now = datetime.now()
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now
        )
        
        # Store and return
        return self.storage.add(task)
    
    def list_tasks(self) -> List[Task]:
        """
        Get all tasks sorted by ID.
        
        Returns:
            List of all Task objects.
        
        Example:
            >>> ops = TodoOperations(TaskStorage())
            >>> ops.add_task("Task 1")
            >>> ops.add_task("Task 2")
            >>> len(ops.list_tasks())
            2
        """
        return self.storage.list_all()
    
    def get_task(self, task_id: int) -> Task:
        """
        Get a task by ID.
        
        Args:
            task_id: The ID of the task to retrieve.
        
        Returns:
            The Task object.
        
        Raises:
            ValueError: If task with given ID is not found.
        
        Example:
            >>> ops = TodoOperations(TaskStorage())
            >>> task = ops.add_task("Test")
            >>> ops.get_task(1).title
            'Test'
            >>> ops.get_task(999)
            Traceback (most recent call last):
            ...
            ValueError: Task with ID 999 not found
        """
        task = self.storage.get(task_id)
        
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")
        
        return task
    
    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update an existing task's title and/or description.
        
        Args:
            task_id: The ID of the task to update.
            title: New title (optional, use existing if None).
            description: New description (optional, use existing if None).
        
        Returns:
            The updated Task object.
        
        Raises:
            ValueError: If task not found or validation fails.
        
        Example:
            >>> ops = TodoOperations(TaskStorage())
            >>> ops.add_task("Old title")
            >>> updated = ops.update_task(1, title="New title")
            >>> updated.title
            'New title'
        """
        # Get existing task
        task = self.get_task(task_id)
        
        # Update title if provided
        if title is not None:
            task.title = validate_title(title)
        
        # Update description if provided
        if description is not None:
            task.description = validate_description(description)
        
        # Update timestamp
        task.updated_at = datetime.now()
        
        # Store and return
        return self.storage.update(task)
    
    def delete_task(self, task_id: int) -> Task:
        """
        Delete a task by ID.
        
        Args:
            task_id: The ID of the task to delete.
        
        Returns:
            The deleted Task object.
        
        Raises:
            ValueError: If task with given ID is not found.
        
        Example:
            >>> ops = TodoOperations(TaskStorage())
            >>> ops.add_task("Test")
            >>> deleted = ops.delete_task(1)
            >>> deleted.title
            'Test'
            >>> len(ops.list_tasks())
            0
        """
        # Verify task exists first
        task = self.get_task(task_id)
        
        # Delete and return
        self.storage.delete(task_id)
        return task
    
    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggle the completion status of a task.
        
        Args:
            task_id: The ID of the task to toggle.
        
        Returns:
            The updated Task object with toggled status.
        
        Raises:
            ValueError: If task with given ID is not found.
        
        Example:
            >>> ops = TodoOperations(TaskStorage())
            >>> ops.add_task("Test")
            >>> task = ops.toggle_complete(1)
            >>> task.completed
            True
            >>> task = ops.toggle_complete(1)
            >>> task.completed
            False
        """
        # Get existing task
        task = self.get_task(task_id)
        
        # Toggle status
        task.completed = not task.completed
        
        # Update timestamp
        task.updated_at = datetime.now()
        
        # Store and return
        return self.storage.update(task)
    
    def get_stats(self) -> dict:
        """
        Get task statistics.
        
        Returns:
            Dictionary with total, completed, and pending counts.
        
        Example:
            >>> ops = TodoOperations(TaskStorage())
            >>> ops.add_task("Task 1")
            >>> ops.add_task("Task 2")
            >>> ops.toggle_complete(1)
            >>> stats = ops.get_stats()
            >>> stats['total']
            2
            >>> stats['completed']
            1
        """
        tasks = self.list_tasks()
        completed = sum(1 for t in tasks if t.completed)
        
        return {
            'total': len(tasks),
            'completed': completed,
            'pending': len(tasks) - completed
        }
