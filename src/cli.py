"""
Command Line Interface Module

Provides the user interface for the Todo Console Application.
Handles all input/output and delegates operations to TodoOperations.

Reference: specs/001-console-app/spec.md
"""

import sys
from typing import Optional
from src.models import Task
from src.storage import TaskStorage
from src.operations import TodoOperations


# ============================================================================
# Display Functions
# ============================================================================

def display_menu() -> None:
    """Display the main menu with options."""
    print()
    print("╔════════════════════════════════════════╗")
    print("║         📝 TODO CONSOLE APP            ║")
    print("╠════════════════════════════════════════╣")
    print("║  [1] ➕ Add Task                       ║")
    print("║  [2] 📋 List Tasks                     ║")
    print("║  [3] ✏️  Update Task                    ║")
    print("║  [4] 🗑️  Delete Task                    ║")
    print("║  [5] ✅ Toggle Complete                ║")
    print("║  [6] 🚪 Exit                           ║")
    print("╚════════════════════════════════════════╝")
    print()


def display_task(task: Task, detailed: bool = False) -> None:
    """
    Display a single task.
    
    Args:
        task: The Task object to display.
        detailed: If True, show description and timestamps.
    """
    status = "✓" if task.completed else "○"
    status_color = "completed" if task.completed else "pending"
    
    print(f"  #{task.id} {status} {task.title}")
    
    if detailed:
        if task.description:
            print(f"     📝 {task.description}")
        print(f"     📅 Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        if task.updated_at != task.created_at:
            print(f"     🔄 Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")


def display_task_list(tasks: list[Task]) -> None:
    """
    Display all tasks in a formatted list.
    
    Args:
        tasks: List of Task objects to display.
    """
    if not tasks:
        print()
        print("  📭 No tasks yet! Add one with option [1]")
        print()
        return
    
    print()
    print("┌─────────────────────────────────────────┐")
    print("│              YOUR TASKS                 │")
    print("├─────────────────────────────────────────┤")
    
    for task in tasks:
        status = "✓" if task.completed else "○"
        title = task.title[:35] + "..." if len(task.title) > 35 else task.title
        print(f"│  {status} #{task.id:3d} {title:<33} │")
    
    print("└─────────────────────────────────────────┘")
    
    # Calculate stats
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    pending = total - completed
    
    print()
    print(f"📊 Total: {total} | ✅ Completed: {completed} | ⏳ Pending: {pending}")
    print()


def display_success(message: str) -> None:
    """Display a success message."""
    print(f"\n✅ {message}\n")


def display_error(message: str) -> None:
    """Display an error message."""
    print(f"\n❌ {message}\n")


def display_info(message: str) -> None:
    """Display an info message."""
    print(f"\nℹ️  {message}\n")


def get_input(prompt: str) -> str:
    """
    Get input from user with a prompt.
    
    Args:
        prompt: The prompt to display.
    
    Returns:
        The user input string (stripped).
    """
    return input(prompt).strip()


def get_int_input(prompt: str) -> Optional[int]:
    """
    Get an integer input from user.
    
    Args:
        prompt: The prompt to display.
    
    Returns:
        The integer value, or None if invalid.
    """
    try:
        value = input(prompt).strip()
        return int(value)
    except ValueError:
        return None


# ============================================================================
# Handler Functions
# ============================================================================

def handle_add_task(ops: TodoOperations) -> None:
    """Handle adding a new task."""
    print("\n➕ ADD NEW TASK")
    print("-" * 40)
    
    # Get title (required)
    title = get_input("Enter task title (required): ")
    
    if not title:
        display_error("Title is required!")
        return
    
    # Get description (optional)
    description = get_input("Enter description (optional, press Enter to skip): ")
    description = description if description else None
    
    try:
        task = ops.add_task(title, description)
        display_success(f"Task created successfully!")
        print("  Created task:")
        display_task(task, detailed=True)
    except ValueError as e:
        display_error(str(e))


def handle_list_tasks(ops: TodoOperations) -> None:
    """Handle listing all tasks."""
    tasks = ops.list_tasks()
    display_task_list(tasks)


def handle_update_task(ops: TodoOperations) -> None:
    """Handle updating an existing task."""
    print("\n✏️  UPDATE TASK")
    print("-" * 40)
    
    # Get task ID
    task_id = get_int_input("Enter task ID to update: ")
    
    if task_id is None:
        display_error("Please enter a valid number")
        return
    
    try:
        # Get and display current task
        task = ops.get_task(task_id)
        print("\nCurrent task details:")
        display_task(task, detailed=True)
        print()
        
        # Get new values
        print("(Press Enter to keep current value)")
        new_title = get_input(f"New title [{task.title}]: ")
        
        current_desc = task.description or "(none)"
        new_description = get_input(f"New description [{current_desc}]: ")
        
        # Check if anything changed
        title_to_update = new_title if new_title else None
        desc_to_update = new_description if new_description else None
        
        if title_to_update is None and desc_to_update is None:
            display_info("No changes made")
            return
        
        # Update task
        updated = ops.update_task(
            task_id,
            title=title_to_update,
            description=desc_to_update
        )
        
        display_success("Task updated successfully!")
        print("  Updated task:")
        display_task(updated, detailed=True)
        
    except ValueError as e:
        display_error(str(e))


def handle_delete_task(ops: TodoOperations) -> None:
    """Handle deleting a task."""
    print("\n🗑️  DELETE TASK")
    print("-" * 40)
    
    # Get task ID
    task_id = get_int_input("Enter task ID to delete: ")
    
    if task_id is None:
        display_error("Please enter a valid number")
        return
    
    try:
        # Get and display task
        task = ops.get_task(task_id)
        print("\nTask to delete:")
        display_task(task, detailed=True)
        print()
        
        # Confirm deletion
        confirm = get_input("Are you sure you want to delete this task? (y/n): ")
        
        if confirm.lower() in ('y', 'yes'):
            ops.delete_task(task_id)
            display_success(f"Task #{task_id} deleted successfully!")
        else:
            display_info("Deletion cancelled")
            
    except ValueError as e:
        display_error(str(e))


def handle_toggle_complete(ops: TodoOperations) -> None:
    """Handle toggling task completion status."""
    print("\n✅ TOGGLE COMPLETION STATUS")
    print("-" * 40)
    
    # Get task ID
    task_id = get_int_input("Enter task ID to toggle: ")
    
    if task_id is None:
        display_error("Please enter a valid number")
        return
    
    try:
        # Toggle and display result
        task = ops.toggle_complete(task_id)
        
        if task.completed:
            display_success(f"Task #{task_id} marked as COMPLETE! 🎉")
        else:
            display_success(f"Task #{task_id} marked as INCOMPLETE")
        
        display_task(task, detailed=True)
        
    except ValueError as e:
        display_error(str(e))


# ============================================================================
# Main Application
# ============================================================================

def main() -> None:
    """
    Main entry point for the Todo Console Application.
    
    Runs the main menu loop until the user chooses to exit.
    Handles keyboard interrupt (Ctrl+C) gracefully.
    """
    # Initialize components
    storage = TaskStorage()
    ops = TodoOperations(storage)
    
    # Welcome message
    print("\n" + "=" * 42)
    print("   Welcome to the Todo Console App! 📝")
    print("   Phase I - In-Memory Storage")
    print("=" * 42)
    
    # Main loop
    try:
        while True:
            display_menu()
            
            choice = get_input("Enter your choice (1-6): ")
            
            match choice:
                case "1":
                    handle_add_task(ops)
                case "2":
                    handle_list_tasks(ops)
                case "3":
                    handle_update_task(ops)
                case "4":
                    handle_delete_task(ops)
                case "5":
                    handle_toggle_complete(ops)
                case "6":
                    print("\n👋 Goodbye! Your tasks are not saved (in-memory only).\n")
                    sys.exit(0)
                case _:
                    display_error("Invalid choice. Please enter 1-6")
                    
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
