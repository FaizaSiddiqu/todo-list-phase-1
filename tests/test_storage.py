"""
Tests for Task Storage

Tests the TaskStorage class functionality.
"""

import pytest
from src.models import Task
from src.storage import TaskStorage


class TestGenerateId:
    """Tests for ID generation."""
    
    def test_generate_id_starts_at_one(self, storage: TaskStorage):
        """First generated ID should be 1."""
        assert storage.generate_id() == 1
    
    def test_generate_id_increments(self, storage: TaskStorage):
        """IDs should increment with each call."""
        id1 = storage.generate_id()
        id2 = storage.generate_id()
        id3 = storage.generate_id()
        
        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
    
    def test_generate_id_continues_after_delete(self, storage: TaskStorage):
        """ID counter should not reset after deleting tasks."""
        id1 = storage.generate_id()
        task = Task(id=id1, title="Test")
        storage.add(task)
        storage.delete(id1)
        
        id2 = storage.generate_id()
        assert id2 == 2


class TestAddTask:
    """Tests for adding tasks."""
    
    def test_add_task_stores_task(self, storage: TaskStorage):
        """Adding a task should store it in storage."""
        task = Task(id=1, title="Test task")
        result = storage.add(task)
        
        assert result == task
        assert storage.get(1) == task
    
    def test_add_task_returns_task(self, storage: TaskStorage):
        """Adding should return the stored task."""
        task = Task(id=1, title="Test task")
        result = storage.add(task)
        
        assert result is task
    
    def test_add_multiple_tasks(self, storage: TaskStorage):
        """Multiple tasks can be added."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")
        
        storage.add(task1)
        storage.add(task2)
        
        assert storage.count() == 2
        assert storage.get(1) == task1
        assert storage.get(2) == task2


class TestGetTask:
    """Tests for retrieving tasks."""
    
    def test_get_existing_task(self, storage: TaskStorage):
        """Getting an existing task returns it."""
        task = Task(id=1, title="Test task")
        storage.add(task)
        
        result = storage.get(1)
        assert result == task
    
    def test_get_nonexistent_task_returns_none(self, storage: TaskStorage):
        """Getting a non-existent task returns None."""
        result = storage.get(999)
        assert result is None
    
    def test_get_from_empty_storage(self, storage: TaskStorage):
        """Getting from empty storage returns None."""
        result = storage.get(1)
        assert result is None


class TestUpdateTask:
    """Tests for updating tasks."""
    
    def test_update_task(self, storage: TaskStorage):
        """Updating a task modifies it in storage."""
        task = Task(id=1, title="Original")
        storage.add(task)
        
        task.title = "Updated"
        storage.update(task)
        
        result = storage.get(1)
        assert result.title == "Updated"
    
    def test_update_returns_task(self, storage: TaskStorage):
        """Update returns the updated task."""
        task = Task(id=1, title="Test")
        storage.add(task)
        
        task.completed = True
        result = storage.update(task)
        
        assert result.completed is True


class TestDeleteTask:
    """Tests for deleting tasks."""
    
    def test_delete_existing_task(self, storage: TaskStorage):
        """Deleting an existing task removes it."""
        task = Task(id=1, title="Test")
        storage.add(task)
        
        result = storage.delete(1)
        
        assert result == task
        assert storage.get(1) is None
    
    def test_delete_returns_deleted_task(self, storage: TaskStorage):
        """Delete returns the removed task."""
        task = Task(id=1, title="Test")
        storage.add(task)
        
        result = storage.delete(1)
        assert result == task
    
    def test_delete_nonexistent_task_returns_none(self, storage: TaskStorage):
        """Deleting non-existent task returns None."""
        result = storage.delete(999)
        assert result is None
    
    def test_delete_reduces_count(self, storage: TaskStorage):
        """Deleting a task reduces the count."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")
        storage.add(task1)
        storage.add(task2)
        
        assert storage.count() == 2
        storage.delete(1)
        assert storage.count() == 1


class TestListAll:
    """Tests for listing all tasks."""
    
    def test_list_all_empty(self, storage: TaskStorage):
        """Listing empty storage returns empty list."""
        result = storage.list_all()
        assert result == []
    
    def test_list_all_with_tasks(self, storage: TaskStorage):
        """Listing returns all stored tasks."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")
        storage.add(task1)
        storage.add(task2)
        
        result = storage.list_all()
        assert len(result) == 2
        assert task1 in result
        assert task2 in result
    
    def test_list_all_sorted_by_id(self, storage: TaskStorage):
        """Listing returns tasks sorted by ID."""
        # Add in non-sequential order
        task3 = Task(id=3, title="Task 3")
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")
        storage.add(task3)
        storage.add(task1)
        storage.add(task2)
        
        result = storage.list_all()
        assert [t.id for t in result] == [1, 2, 3]


class TestClear:
    """Tests for clearing storage."""
    
    def test_clear_removes_all(self, storage: TaskStorage):
        """Clear removes all tasks."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2")
        storage.add(task1)
        storage.add(task2)
        
        storage.clear()
        
        assert storage.count() == 0
        assert storage.list_all() == []
    
    def test_clear_resets_id_counter(self, storage: TaskStorage):
        """Clear resets the ID counter."""
        storage.generate_id()
        storage.generate_id()
        
        storage.clear()
        
        assert storage.generate_id() == 1


class TestCount:
    """Tests for counting tasks."""
    
    def test_count_empty(self, storage: TaskStorage):
        """Empty storage has count 0."""
        assert storage.count() == 0
    
    def test_count_with_tasks(self, storage: TaskStorage):
        """Count reflects number of tasks."""
        storage.add(Task(id=1, title="Task 1"))
        assert storage.count() == 1
        
        storage.add(Task(id=2, title="Task 2"))
        assert storage.count() == 2
