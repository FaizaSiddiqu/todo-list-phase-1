"""
Task Storage Module

Provides in-memory storage for Task objects with CRUD operations.
This module handles data persistence within the application session.

Reference: specs/001-console-app/plan.md
"""

from typing import List, Optional
from src.models import Task


class TaskStorage:
    """
    In-memory storage for Task objects.
    
    Uses a dictionary for O(1) lookup by task ID.
    Maintains an auto-increment counter for generating unique IDs.
    
    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects.
        _next_id: Counter for generating the next unique ID.
    
    Example:
        >>> storage = TaskStorage()
        >>> task = Task(id=storage.generate_id(), title="Test")
        >>> storage.add(task)
        >>> storage.get(1).title
        'Test'
    """
    
    def __init__(self) -> None:
        """Initialize empty storage with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    def generate_id(self) -> int:
        """
        Generate the next unique task ID.
        
        Returns:
            The next available integer ID.
        
        Example:
            >>> storage = TaskStorage()
            >>> storage.generate_id()
            1
            >>> storage.generate_id()
            2
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id
    
    def add(self, task: Task) -> Task:
        """
        Add a task to storage.
        
        Args:
            task: The Task object to store.
        
        Returns:
            The stored Task object.
        
        Example:
            >>> storage = TaskStorage()
            >>> task = Task(id=1, title="Test")
            >>> stored = storage.add(task)
            >>> stored.id
            1
        """
        self._tasks[task.id] = task
        return task
    
    def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: The ID of the task to retrieve.
        
        Returns:
            The Task object if found, None otherwise.
        
        Example:
            >>> storage = TaskStorage()
            >>> storage.get(999) is None
            True
        """
        return self._tasks.get(task_id)
    
    def update(self, task: Task) -> Task:
        """
        Update an existing task in storage.
        
        Args:
            task: The Task object with updated values.
        
        Returns:
            The updated Task object.
        
        Note:
            Assumes the task exists. Use get() first to verify.
        """
        self._tasks[task.id] = task
        return task
    
    def delete(self, task_id: int) -> Optional[Task]:
        """
        Remove a task from storage.
        
        Args:
            task_id: The ID of the task to remove.
        
        Returns:
            The removed Task object if found, None otherwise.
        
        Example:
            >>> storage = TaskStorage()
            >>> task = Task(id=1, title="Test")
            >>> storage.add(task)
            >>> deleted = storage.delete(1)
            >>> deleted.title
            'Test'
            >>> storage.get(1) is None
            True
        """
        return self._tasks.pop(task_id, None)
    
    def list_all(self) -> List[Task]:
        """
        Get all tasks sorted by ID.
        
        Returns:
            List of all Task objects, sorted by ID ascending.
        
        Example:
            >>> storage = TaskStorage()
            >>> storage.add(Task(id=2, title="Second"))
            >>> storage.add(Task(id=1, title="First"))
            >>> [t.id for t in storage.list_all()]
            [1, 2]
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)
    
    def count(self) -> int:
        """
        Get the number of tasks in storage.
        
        Returns:
            The count of stored tasks.
        """
        return len(self._tasks)
    
    def clear(self) -> None:
        """
        Remove all tasks and reset the ID counter.
        
        Useful for testing to ensure clean state.
        """
        self._tasks.clear()
        self._next_id = 1
