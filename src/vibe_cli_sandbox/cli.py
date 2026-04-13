"""Main CLI entry point for vibe command."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path
from typing import Optional
import uuid

from .models import TaskConfig, TaskResult

app = typer.Typer(help="Vibe CLI Sandbox - AI-powered code assistance")
console = Console()


@app.command()
def run(
    repo: str = typer.Option(..., "--repo", help="Repository path or URL"),
    task: str = typer.Option(..., "--task", help="Task description"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output markdown file"),
    json_out: Optional[Path] = typer.Option(None, "--json-out", help="Output JSON file"),
):
    """
    Run a vibe task on a repository.
    """
    console.print(Panel.fit(
        f"[bold cyan]Vibe Task Runner[/bold cyan]\n"
        f"Repo: {repo}\n"
        f"Task: {task}",
        title="🚀 Starting"
    ))

    config = TaskConfig(repo_path=repo, task_description=task)

        # Week2: input validation (invalid_input)
    if not task.strip():
        fail = TaskResult(
            request_id=uuid.uuid4().hex,
            success=False,
            message="Invalid input: --task is empty",
            timings_ms={"total_ms": 0.0},
            error={
                "type": "invalid_input",
                "message": "Invalid input: --task is empty",
                "details": None,
            },
            # Week2: structure must be stable even on failure
            commands=[],
            risks=[],
            fallback=[
                "Provide a non-empty --task string.",
                'Example: vibe run --repo . --task "timing smoke test" --json-out out.json',
            ],
        )

        if json_out:
            json_out.write_text(fail.to_json())
            console.print(f"[blue]📊 JSON output written to: {json_out}[/blue]")

        raise typer.Exit(1)

    try:
        from .runner import run_task
        result = run_task(config)

        # Display results
        console.print(f"\n[green]✅ Task completed![/green]")
        console.print(f"Changes: {len(result.changes)} files modified")

        # Create table of changes
        if result.changes:
            table = Table(title="Changes Made")
            table.add_column("File", style="cyan")
            table.add_column("Summary", style="white")
            for change in result.changes[:5]:  # Show first 5
                table.add_row(change.file, change.summary[:50])
            console.print(table)

        # Write output files
        if out:
            out.write_text(result.to_markdown())
            console.print(f"\n[blue]📝 Markdown output written to: {out}[/blue]")

        if json_out:
            json_out.write_text(result.to_json())
            console.print(f"[blue]📊 JSON output written to: {json_out}[/blue]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

        # If user requested JSON output, write a structured failure result
        if json_out:
            fail = TaskResult(
                request_id=uuid.uuid4().hex,
                success=False,
                message=str(e),
                timings_ms={"total_ms": 0.0},
                error={
                    "type": "runtime_error",
                    "message":str(e),
                    "details":None,
                    commands:[],
                    risks:[],
                    fallback:[ "Re-run with a simpler task.", "Check your environment and dependencies." ],
                }
            )
            json_out.write_text(fail.to_json())
            console.print(f"[blue]📊 JSON output written to: {json_out}[/blue]")

        raise typer.Exit(1)


@app.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(f"[bold]Vibe CLI Sandbox[/bold] version {__version__}")


if __name__ == "__main__":
    app()
