"""
Test Configuration and Fixtures

Provides shared fixtures for all test modules.
"""

import pytest
from datetime import datetime
from src.models import Task
from src.storage import TaskStorage
from src.operations import TodoOperations


@pytest.fixture
def storage() -> TaskStorage:
    """Provide a fresh TaskStorage instance for each test."""
    return TaskStorage()


@pytest.fixture
def operations(storage: TaskStorage) -> TodoOperations:
    """Provide a TodoOperations instance with fresh storage."""
    return TodoOperations(storage)


@pytest.fixture
def sample_task() -> Task:
    """Provide a sample Task object for testing."""
    return Task(
        id=1,
        title="Sample Task",
        description="Sample description",
        completed=False,
        created_at=datetime(2026, 1, 3, 10, 0, 0),
        updated_at=datetime(2026, 1, 3, 10, 0, 0)
    )


@pytest.fixture
def populated_storage(storage: TaskStorage) -> TaskStorage:
    """Provide a storage with some pre-populated tasks."""
    tasks = [
        Task(id=storage.generate_id(), title="Task 1", completed=False),
        Task(id=storage.generate_id(), title="Task 2", completed=True),
        Task(id=storage.generate_id(), title="Task 3", description="With description"),
    ]
    for task in tasks:
        storage.add(task)
    return storage


@pytest.fixture
def populated_operations(populated_storage: TaskStorage) -> TodoOperations:
    """Provide TodoOperations with pre-populated storage."""
    return TodoOperations(populated_storage)
