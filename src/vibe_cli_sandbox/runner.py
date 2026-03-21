"""Core task runner logic."""

from pathlib import Path
from .models import TaskConfig, TaskResult, Change

def run_task(config: TaskConfig) -> TaskResult:
    """
    Execute a vibe task on the repository.
    
    This is a mock implementation that simulates running a task.
    In a real implementation, this would analyze the repo and make changes.
    """
    repo_path = Path(config.repo_path)
    
    # Check if repo exists
    if not repo_path.exists():
        return TaskResult(
            success=False,
            message=f"Repository path not found: {repo_path}"
        )
    
    # Mock task execution
    result = TaskResult(
        success=True,
        message=f"Successfully processed task: {config.task_description[:100]}"
    )
    
    # Mock changes (for demonstration)
    # In reality, this would come from actual AI processing
    result.changes = [
        Change(
            file="README.md",
            summary="Updated documentation with task information",
            diff=f"+ # Task: {config.task_description}\n+ This task was processed by vibe."
        ),
        Change(
            file="src/main.py",
            summary="Added logging for task execution",
            diff="+ import logging\n+ logging.info('Task executed')"
        )
    ]
    
    return result
