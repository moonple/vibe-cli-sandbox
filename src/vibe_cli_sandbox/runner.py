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

"""Core task runner logic."""

from pathlib import Path
import time
import uuid

from .models import TaskConfig, TaskResult, Change, ErrorInfo


def run_task(config: TaskConfig) -> TaskResult:
    """
    Execute a vibe task on the repository.

    This is a mock implementation that simulates running a task.
    In a real implementation, this would analyze the repo and make changes.
    """
    t0 = time.perf_counter()
    request_id = uuid.uuid4().hex

    timings_ms: dict[str, float] = {}

    # Validate repo path
    tv0 = time.perf_counter()
    repo_path = Path(config.repo_path)
    if not repo_path.exists():
        timings_ms["validate_repo_ms"] = (time.perf_counter() - tv0) * 1000.0
        timings_ms["total_ms"] = (time.perf_counter() - t0) * 1000.0
        return TaskResult(
            request_id=request_id,
            success=False,
            message=f"Repository path not found: {repo_path}",
            timings_ms=timings_ms,
            error=ErrorInfo(
                type="repo_not_found",
                message=f"Repository path not found: {repo_path}",
            ),
        )
    timings_ms["validate_repo_ms"] = (time.perf_counter() - tv0) * 1000.0

    # Mock task execution
    tg0 = time.perf_counter()
    result = TaskResult(
        request_id=request_id,
        success=True,
        message=f"Successfully processed task: {config.task_description[:100]}",
    )

    # Mock changes (for demonstration)
    result.changes = [
        Change(
            file="README.md",
            summary="Updated documentation with task information",
            diff=f"+ # Task: {config.task_description}\n+ This task was processed by vibe.",
        ),
        Change(
            file="src/main.py",
            summary="Added logging for task execution",
            diff="+ import logging\n+ logging.info('Task executed')",
        ),
    ]
    timings_ms["mock_generate_ms"] = (time.perf_counter() - tg0) * 1000.0

    timings_ms["total_ms"] = (time.perf_counter() - t0) * 1000.0
    result.timings_ms = timings_ms
    return result
