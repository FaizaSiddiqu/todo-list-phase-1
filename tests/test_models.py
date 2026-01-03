"""
Tests for Task Model

Tests the Task dataclass functionality.
"""

import pytest
from datetime import datetime
from src.models import Task


class TestTaskCreation:
    """Tests for Task instantiation."""
    
    def test_create_task_with_required_fields(self):
        """Task can be created with just id and title."""
        task = Task(id=1, title="Test task")
        
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description is None
        assert task.completed is False
    
    def test_create_task_with_all_fields(self):
        """Task can be created with all fields specified."""
        created = datetime(2026, 1, 1, 12, 0, 0)
        updated = datetime(2026, 1, 2, 12, 0, 0)
        
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            completed=True,
            created_at=created,
            updated_at=updated
        )
        
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.completed is True
        assert task.created_at == created
        assert task.updated_at == updated
    
    def test_default_completed_is_false(self):
        """Default completed status is False."""
        task = Task(id=1, title="Test")
        assert task.completed is False
    
    def test_default_description_is_none(self):
        """Default description is None."""
        task = Task(id=1, title="Test")
        assert task.description is None
    
    def test_timestamps_auto_set(self):
        """Timestamps are automatically set to current time."""
        before = datetime.now()
        task = Task(id=1, title="Test")
        after = datetime.now()
        
        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after


class TestTaskStringRepresentation:
    """Tests for Task string methods."""
    
    def test_str_incomplete_task(self):
        """String representation shows circle for incomplete task."""
        task = Task(id=1, title="Test task", completed=False)
        result = str(task)
        
        assert "○" in result
        assert "#1" in result
        assert "Test task" in result
    
    def test_str_complete_task(self):
        """String representation shows checkmark for complete task."""
        task = Task(id=1, title="Test task", completed=True)
        result = str(task)
        
        assert "✓" in result
        assert "#1" in result
        assert "Test task" in result


class TestTaskEquality:
    """Tests for Task equality comparisons."""
    
    def test_tasks_with_same_values_are_equal(self):
        """Two tasks with same values are equal."""
        created = datetime(2026, 1, 1)
        task1 = Task(id=1, title="Test", created_at=created, updated_at=created)
        task2 = Task(id=1, title="Test", created_at=created, updated_at=created)
        
        assert task1 == task2
    
    def test_tasks_with_different_ids_not_equal(self):
        """Tasks with different IDs are not equal."""
        created = datetime(2026, 1, 1)
        task1 = Task(id=1, title="Test", created_at=created, updated_at=created)
        task2 = Task(id=2, title="Test", created_at=created, updated_at=created)
        
        assert task1 != task2
