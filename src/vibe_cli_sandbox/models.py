"""Data models for vibe tasks."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class TaskConfig(BaseModel):
    """Configuration for a vibe task."""
    repo_path: str = Field(..., description="Path to the repository")
    task_description: str = Field(..., description="Task to perform")


class Change(BaseModel):
    """Represents a single file change."""
    file: str
    summary: str
    diff: Optional[str] = None


class ErrorInfo(BaseModel):
    """Structured error information for observability/eval."""
    type: str
    message: str
    details: Optional[str] = None


class TaskResult(BaseModel):
    """Result of running a vibe task."""
    request_id: str = ""
    success: bool = True
    message: str = ""
    changes: List[Change] = Field(default_factory=list)

    # Observability fields (written into out.json)
    timings_ms: Dict[str, float] = Field(default_factory=dict)
    error: Optional[ErrorInfo] = None

    def to_markdown(self) -> str:
        """Convert result to markdown format."""
        lines = ["# Vibe Task Result\n"]
        lines.append(f"**Status:** {'✅ Success' if self.success else '❌ Failed'}\n")
        if self.message:
            lines.append(f"**Message:** {self.message}\n")
        if self.changes:
            lines.append("## Changes Made\n")
            for change in self.changes:
                lines.append(f"### {change.file}\n")
                lines.append(f"{change.summary}\n")
                if change.diff:
                    lines.append("```diff\n")
                    lines.append(change.diff)
                    lines.append("\n```\n")
        return "\n".join(lines)

    def to_json(self) -> str:
        """Convert result to JSON format."""
        import json
        return json.dumps(self.model_dump(), indent=2, ensure_ascii=False)
