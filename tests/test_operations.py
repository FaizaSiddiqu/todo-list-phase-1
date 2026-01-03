"""
Tests for Todo Operations

Tests the TodoOperations class and validation functions.
"""

import pytest
from datetime import datetime
import time
from src.storage import TaskStorage
from src.operations import (
    TodoOperations,
    validate_title,
    validate_description,
    TITLE_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH
)


# ============================================================================
# Validation Function Tests
# ============================================================================

class TestValidateTitle:
    """Tests for title validation."""
    
    def test_valid_title(self):
        """Valid title is returned stripped."""
        assert validate_title("  Buy groceries  ") == "Buy groceries"
    
    def test_empty_title_raises(self):
        """Empty title raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_title("")
    
    def test_whitespace_only_title_raises(self):
        """Whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_title("   ")
    
    def test_title_at_max_length(self):
        """Title at max length is valid."""
        title = "a" * TITLE_MAX_LENGTH
        assert validate_title(title) == title
    
    def test_title_too_long_raises(self):
        """Title exceeding max length raises ValueError."""
        title = "a" * (TITLE_MAX_LENGTH + 1)
        with pytest.raises(ValueError, match="200 characters or less"):
            validate_title(title)


class TestValidateDescription:
    """Tests for description validation."""
    
    def test_valid_description(self):
        """Valid description is returned stripped."""
        assert validate_description("  Details here  ") == "Details here"
    
    def test_none_description(self):
        """None description returns None."""
        assert validate_description(None) is None
    
    def test_empty_description_becomes_none(self):
        """Empty string becomes None."""
        assert validate_description("") is None
    
    def test_whitespace_description_becomes_none(self):
        """Whitespace-only becomes None."""
        assert validate_description("   ") is None
    
    def test_description_at_max_length(self):
        """Description at max length is valid."""
        desc = "a" * DESCRIPTION_MAX_LENGTH
        assert validate_description(desc) == desc
    
    def test_description_too_long_raises(self):
        """Description exceeding max length raises ValueError."""
        desc = "a" * (DESCRIPTION_MAX_LENGTH + 1)
        with pytest.raises(ValueError, match="1000 characters or less"):
            validate_description(desc)


# ============================================================================
# Add Task Tests
# ============================================================================

class TestAddTask:
    """Tests for adding tasks."""
    
    def test_add_task_valid(self, operations: TodoOperations):
        """Adding a valid task returns the task."""
        task = operations.add_task("Buy groceries")
        
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.completed is False
    
    def test_add_task_with_description(self, operations: TodoOperations):
        """Task can be created with description."""
        task = operations.add_task("Buy groceries", "Milk, eggs, bread")
        
        assert task.description == "Milk, eggs, bread"
    
    def test_add_task_strips_whitespace(self, operations: TodoOperations):
        """Title and description are stripped."""
        task = operations.add_task("  Buy groceries  ", "  Details  ")
        
        assert task.title == "Buy groceries"
        assert task.description == "Details"
    
    def test_add_task_empty_description_becomes_none(self, operations: TodoOperations):
        """Empty description becomes None."""
        task = operations.add_task("Test", "   ")
        
        assert task.description is None
    
    def test_add_task_empty_title_raises(self, operations: TodoOperations):
        """Empty title raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            operations.add_task("")
    
    def test_add_task_title_too_long_raises(self, operations: TodoOperations):
        """Title too long raises ValueError."""
        with pytest.raises(ValueError):
            operations.add_task("a" * 201)
    
    def test_add_task_description_too_long_raises(self, operations: TodoOperations):
        """Description too long raises ValueError."""
        with pytest.raises(ValueError):
            operations.add_task("Valid title", "a" * 1001)
    
    def test_add_task_auto_increments_id(self, operations: TodoOperations):
        """Task IDs auto-increment."""
        task1 = operations.add_task("Task 1")
        task2 = operations.add_task("Task 2")
        task3 = operations.add_task("Task 3")
        
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
    
    def test_add_task_sets_timestamps(self, operations: TodoOperations):
        """Timestamps are set on creation."""
        before = datetime.now()
        task = operations.add_task("Test")
        after = datetime.now()
        
        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after


# ============================================================================
# List Tasks Tests
# ============================================================================

class TestListTasks:
    """Tests for listing tasks."""
    
    def test_list_tasks_empty(self, operations: TodoOperations):
        """Empty storage returns empty list."""
        result = operations.list_tasks()
        assert result == []
    
    def test_list_tasks_with_tasks(self, operations: TodoOperations):
        """Returns all tasks."""
        operations.add_task("Task 1")
        operations.add_task("Task 2")
        
        result = operations.list_tasks()
        assert len(result) == 2
    
    def test_list_tasks_sorted_by_id(self, operations: TodoOperations):
        """Tasks are sorted by ID."""
        operations.add_task("First")
        operations.add_task("Second")
        operations.add_task("Third")
        
        result = operations.list_tasks()
        ids = [t.id for t in result]
        assert ids == [1, 2, 3]


# ============================================================================
# Get Task Tests
# ============================================================================

class TestGetTask:
    """Tests for getting a single task."""
    
    def test_get_task_exists(self, operations: TodoOperations):
        """Getting existing task returns it."""
        created = operations.add_task("Test")
        
        result = operations.get_task(1)
        assert result == created
    
    def test_get_task_not_found_raises(self, operations: TodoOperations):
        """Getting non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            operations.get_task(999)


# ============================================================================
# Update Task Tests
# ============================================================================

class TestUpdateTask:
    """Tests for updating tasks."""
    
    def test_update_task_title(self, operations: TodoOperations):
        """Can update just the title."""
        operations.add_task("Original", "Description")
        
        updated = operations.update_task(1, title="Updated")
        
        assert updated.title == "Updated"
        assert updated.description == "Description"
    
    def test_update_task_description(self, operations: TodoOperations):
        """Can update just the description."""
        operations.add_task("Title", "Original")
        
        updated = operations.update_task(1, description="Updated")
        
        assert updated.title == "Title"
        assert updated.description == "Updated"
    
    def test_update_task_both(self, operations: TodoOperations):
        """Can update both title and description."""
        operations.add_task("Original Title", "Original Desc")
        
        updated = operations.update_task(1, title="New Title", description="New Desc")
        
        assert updated.title == "New Title"
        assert updated.description == "New Desc"
    
    def test_update_task_not_found_raises(self, operations: TodoOperations):
        """Updating non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            operations.update_task(999, title="Test")
    
    def test_update_task_updates_timestamp(self, operations: TodoOperations):
        """Updating task updates the updated_at timestamp."""
        task = operations.add_task("Test")
        original_updated = task.updated_at
        
        # Small delay to ensure timestamp difference
        time.sleep(0.01)
        
        updated = operations.update_task(1, title="Updated")
        
        assert updated.updated_at > original_updated
    
    def test_update_task_validates_title(self, operations: TodoOperations):
        """Update validates new title."""
        operations.add_task("Test")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            operations.update_task(1, title="   ")
    
    def test_update_task_validates_description(self, operations: TodoOperations):
        """Update validates new description."""
        operations.add_task("Test")
        
        with pytest.raises(ValueError):
            operations.update_task(1, description="a" * 1001)


# ============================================================================
# Delete Task Tests
# ============================================================================

class TestDeleteTask:
    """Tests for deleting tasks."""
    
    def test_delete_task_exists(self, operations: TodoOperations):
        """Deleting existing task removes it."""
        operations.add_task("Test")
        
        deleted = operations.delete_task(1)
        
        assert deleted.title == "Test"
        assert len(operations.list_tasks()) == 0
    
    def test_delete_task_not_found_raises(self, operations: TodoOperations):
        """Deleting non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            operations.delete_task(999)
    
    def test_delete_task_returns_deleted(self, operations: TodoOperations):
        """Delete returns the deleted task."""
        original = operations.add_task("Test", "Description")
        
        deleted = operations.delete_task(1)
        
        assert deleted.id == original.id
        assert deleted.title == original.title


# ============================================================================
# Toggle Complete Tests
# ============================================================================

class TestToggleComplete:
    """Tests for toggling completion status."""
    
    def test_toggle_complete_to_true(self, operations: TodoOperations):
        """Toggling incomplete task marks it complete."""
        operations.add_task("Test")
        
        result = operations.toggle_complete(1)
        
        assert result.completed is True
    
    def test_toggle_complete_to_false(self, operations: TodoOperations):
        """Toggling complete task marks it incomplete."""
        operations.add_task("Test")
        operations.toggle_complete(1)  # Make complete
        
        result = operations.toggle_complete(1)  # Toggle back
        
        assert result.completed is False
    
    def test_toggle_complete_not_found_raises(self, operations: TodoOperations):
        """Toggling non-existent task raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            operations.toggle_complete(999)
    
    def test_toggle_complete_updates_timestamp(self, operations: TodoOperations):
        """Toggling updates the updated_at timestamp."""
        task = operations.add_task("Test")
        original_updated = task.updated_at
        
        # Small delay to ensure timestamp difference
        time.sleep(0.01)
        
        toggled = operations.toggle_complete(1)
        
        assert toggled.updated_at > original_updated


# ============================================================================
# Get Stats Tests
# ============================================================================

class TestGetStats:
    """Tests for getting task statistics."""
    
    def test_stats_empty(self, operations: TodoOperations):
        """Empty storage has zero counts."""
        stats = operations.get_stats()
        
        assert stats['total'] == 0
        assert stats['completed'] == 0
        assert stats['pending'] == 0
    
    def test_stats_with_tasks(self, operations: TodoOperations):
        """Stats reflect task states."""
        operations.add_task("Task 1")
        operations.add_task("Task 2")
        operations.add_task("Task 3")
        operations.toggle_complete(1)
        
        stats = operations.get_stats()
        
        assert stats['total'] == 3
        assert stats['completed'] == 1
        assert stats['pending'] == 2
