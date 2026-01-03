"""
Tests for CLI Module

Tests the CLI display functions and helpers.
Note: Interactive menu handlers are tested via integration.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from io import StringIO

from src.models import Task
from src.storage import TaskStorage
from src.operations import TodoOperations
from src import cli


class TestGetIntInput:
    """Tests for get_int_input helper."""
    
    def test_valid_integer_input(self):
        """Valid integer string returns int."""
        with patch('builtins.input', return_value='5'):
            result = cli.get_int_input("Enter ID: ")
            assert result == 5
    
    def test_invalid_returns_none(self):
        """Invalid input returns None."""
        with patch('builtins.input', return_value='abc'):
            result = cli.get_int_input("Enter ID: ")
            assert result is None
    
    def test_empty_returns_none(self):
        """Empty input returns None."""
        with patch('builtins.input', return_value=''):
            result = cli.get_int_input("Enter ID: ")
            assert result is None
    
    def test_negative_returns_value(self):
        """Negative integer is valid."""
        with patch('builtins.input', return_value='-5'):
            result = cli.get_int_input("Enter ID: ")
            assert result == -5


class TestGetInput:
    """Tests for get_input helper."""
    
    def test_strips_whitespace(self):
        """Input is stripped of whitespace."""
        with patch('builtins.input', return_value='  hello  '):
            result = cli.get_input("Enter: ")
            assert result == 'hello'
    
    def test_returns_empty_for_empty(self):
        """Empty input returns empty string."""
        with patch('builtins.input', return_value=''):
            result = cli.get_input("Enter: ")
            assert result == ''


class TestDisplayMenu:
    """Tests for display_menu function."""
    
    def test_display_menu_shows_options(self):
        """Menu displays all options."""
        with patch('builtins.print') as mock_print:
            cli.display_menu()
            
            # Check that something was printed
            assert mock_print.called
            calls = ''.join([str(c) for c in mock_print.call_args_list])
            assert 'TODO' in calls or 'Add' in calls


class TestDisplayTask:
    """Tests for display_task function."""
    
    def test_display_task_incomplete(self):
        """Displays incomplete task correctly."""
        task = Task(
            id=1,
            title="Test Task",
            description="Description",
            completed=False,
            created_at=datetime(2026, 1, 3, 10, 0, 0),
            updated_at=datetime(2026, 1, 3, 10, 0, 0)
        )
        
        with patch('builtins.print') as mock_print:
            cli.display_task(task)
            calls = ''.join([str(c) for c in mock_print.call_args_list])
            assert '#1' in calls or 'Test Task' in calls
    
    def test_display_task_complete(self):
        """Displays complete task correctly."""
        task = Task(
            id=2,
            title="Done Task",
            completed=True,
            created_at=datetime(2026, 1, 3, 10, 0, 0),
            updated_at=datetime(2026, 1, 3, 10, 0, 0)
        )
        
        with patch('builtins.print') as mock_print:
            cli.display_task(task)
            calls = ''.join([str(c) for c in mock_print.call_args_list])
            assert '#2' in calls or 'Done Task' in calls


class TestDisplayTaskList:
    """Tests for display_task_list function."""
    
    def test_empty_list(self):
        """Displays message for empty list."""
        with patch('builtins.print') as mock_print:
            cli.display_task_list([])
            calls = ''.join([str(c) for c in mock_print.call_args_list])
            assert 'No tasks' in calls or 'empty' in calls.lower()
    
    def test_with_tasks(self):
        """Displays all tasks."""
        tasks = [
            Task(id=1, title="Task 1", completed=False),
            Task(id=2, title="Task 2", completed=True),
        ]
        
        with patch('builtins.print') as mock_print:
            cli.display_task_list(tasks)
            assert mock_print.called


class TestDisplayMessages:
    """Tests for display helper functions."""
    
    def test_display_success(self):
        """Success message displays correctly."""
        with patch('builtins.print') as mock_print:
            cli.display_success("Task created!")
            assert mock_print.called
            calls = ''.join([str(c) for c in mock_print.call_args_list])
            assert 'Task created!' in calls
    
    def test_display_error(self):
        """Error message displays correctly."""
        with patch('builtins.print') as mock_print:
            cli.display_error("Invalid input")
            assert mock_print.called
            calls = ''.join([str(c) for c in mock_print.call_args_list])
            assert 'Invalid input' in calls
    
    def test_display_info(self):
        """Info message displays correctly."""
        with patch('builtins.print') as mock_print:
            cli.display_info("Press Enter...")
            assert mock_print.called


class TestHandleAddTask:
    """Tests for handle_add_task."""
    
    def test_add_task_success(self, operations: TodoOperations):
        """Successfully adds a task."""
        with patch('builtins.input', side_effect=['New Task', 'Description']):
            with patch('builtins.print'):
                cli.handle_add_task(operations)
                
                tasks = operations.list_tasks()
                assert len(tasks) == 1
                assert tasks[0].title == 'New Task'
    
    def test_add_task_no_description(self, operations: TodoOperations):
        """Adds task without description."""
        with patch('builtins.input', side_effect=['New Task', '']):
            with patch('builtins.print'):
                cli.handle_add_task(operations)
                
                tasks = operations.list_tasks()
                assert len(tasks) == 1
                assert tasks[0].description is None
    
    def test_add_task_cancelled(self, operations: TodoOperations):
        """Cancelled add doesn't create task."""
        with patch('builtins.input', side_effect=['', '']):  # Empty title
            with patch('builtins.print'):
                cli.handle_add_task(operations)
                
                tasks = operations.list_tasks()
                assert len(tasks) == 0


class TestHandleListTasks:
    """Tests for handle_list_tasks."""
    
    def test_list_empty(self, operations: TodoOperations):
        """List shows empty message."""
        with patch('builtins.print') as mock_print:
            cli.handle_list_tasks(operations)
            assert mock_print.called
    
    def test_list_with_tasks(self, operations: TodoOperations):
        """List shows tasks."""
        operations.add_task("Task 1")
        operations.add_task("Task 2")
        
        with patch('builtins.print') as mock_print:
            cli.handle_list_tasks(operations)
            calls = ''.join([str(c) for c in mock_print.call_args_list])
            assert 'Task 1' in calls or 'Task 2' in calls


class TestHandleUpdateTask:
    """Tests for handle_update_task."""
    
    def test_update_task_success(self, operations: TodoOperations):
        """Successfully updates a task."""
        operations.add_task("Original", "Desc")
        
        with patch('builtins.input', side_effect=['1', 'Updated', 'New Desc']):
            with patch('builtins.print'):
                cli.handle_update_task(operations)
                
                task = operations.get_task(1)
                assert task.title == 'Updated'
                assert task.description == 'New Desc'
    
    def test_update_task_cancel(self, operations: TodoOperations):
        """Cancelled update doesn't modify task."""
        operations.add_task("Original", "Desc")
        
        with patch('builtins.input', side_effect=['0']):  # Cancel
            with patch('builtins.print'):
                cli.handle_update_task(operations)
                
                task = operations.get_task(1)
                assert task.title == 'Original'


class TestHandleDeleteTask:
    """Tests for handle_delete_task."""
    
    def test_delete_task_success(self, operations: TodoOperations):
        """Successfully deletes a task."""
        operations.add_task("To Delete")
        
        with patch('builtins.input', side_effect=['1', 'y']):  # ID=1, confirm=y
            with patch('builtins.print'):
                cli.handle_delete_task(operations)
                
                assert len(operations.list_tasks()) == 0
    
    def test_delete_task_cancel(self, operations: TodoOperations):
        """Cancelled delete keeps task."""
        operations.add_task("Keep Me")
        
        with patch('builtins.input', side_effect=['0']):  # Cancel
            with patch('builtins.print'):
                cli.handle_delete_task(operations)
                
                assert len(operations.list_tasks()) == 1


class TestHandleToggleComplete:
    """Tests for handle_toggle_complete."""
    
    def test_toggle_complete_success(self, operations: TodoOperations):
        """Successfully toggles completion."""
        operations.add_task("Toggle Me")
        
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):
                cli.handle_toggle_complete(operations)
                
                task = operations.get_task(1)
                assert task.completed is True
    
    def test_toggle_complete_invalid_id(self, operations: TodoOperations):
        """Invalid ID shows error."""
        operations.add_task("Stay Incomplete")
        
        with patch('builtins.input', return_value='abc'):
            with patch('builtins.print'):
                cli.handle_toggle_complete(operations)
                
                task = operations.get_task(1)
                assert task.completed is False
