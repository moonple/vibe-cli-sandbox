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

from pathlib import Path

def _write_text_safely(path: Path, content: str) -> None:
    path.write_text(content)

def _write_error_json_fallback(fail_result, requested_json_out: Path | None) -> Path | None:
    """
    Try to write fail_result JSON to requested_json_out; if that fails, write to ./out.error.json.
    Returns the path that was written, or None if nothing was written.
    """
    if requested_json_out is not None:
        try:
            requested_json_out.write_text(fail_result.to_json())
            return requested_json_out
        except Exception:
            fallback_path = Path("out.error.json")
            fallback_path.write_text(fail_result.to_json())
            return fallback_path

    return None

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
        # Week3: observability log summary (always print request_id + total_ms)
        total_ms = None
        try:
            total_ms = result.timings_ms.get("total_ms")
        except Exception:
            total_ms = None
    
        console.print(
            f"\n[bold]Run Summary[/bold]\n"
            f"- request_id: {result.request_id}\n"
            f"- success: {result.success}\n"
            f"- total_ms: {total_ms}\n"
        )

        if not result.success and result.error:
            console.print(
                "[bold red]Failure Details[/bold red]\n"
                f"- error.type: {result.error.type}\n"
                f"- error.message: {result.error.message}\n"
            )
            
        if result.fallback:
                console.print("[bold]Fallback[/bold]")
                for item in result.fallback:
                    console.print(f"- {item}")
        
        # Display results
        if result.success:
            console.print("\n[green]✅ Task completed![/green]")
        else:
            console.print("\n[red]❌ Task failed![/red]")

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
        from .runner import run_task
        result = run_task(config)

        # --- Attempt to write outputs; if it fails, convert to runtime_error and overwrite result ---
        output_write_error = None

        try:
            if out:
                out.write_text(result.to_markdown())
                console.print(f"\n[blue]📝 Markdown output written to: {out}[/blue]")

            if json_out:
                json_out.write_text(result.to_json())
                console.print(f"[blue]📊 JSON output written to: {json_out}[/blue]")

        except Exception as e:
            output_write_error = e

            # Convert to explicit failure result (end-to-end failure)
            result = TaskResult(
                request_id=result.request_id,          # IMPORTANT: keep same request_id
                success=False,
                message=str(e),
                changes=[],                            # optionally keep original result.changes if you prefer
                plan=[],
                commands=[],
                risks=[],
                fallback=[
                    "Choose a writable output path for --json-out/--out.",
                    "Example: --json-out out.json",
                ],
                timings_ms=result.timings_ms,          # keep timings from run_task
                error=ErrorInfo(
                    type="runtime_error",
                    message=str(e),
                    details={"stage": "write_outputs"},
                ),
            )

            # If user requested JSON output, ensure we still persist the failure JSON somewhere
            written_path = _write_error_json_fallback(result, json_out)
            if written_path is not None and written_path != json_out:
                console.print(
                    f"[red]⚠️ Failed to write JSON to {json_out}: {e}[/red]\n"
                    f"[blue]📊 JSON output written to: {written_path}[/blue]"
                )
            elif written_path is not None:
                console.print(f"[blue]📊 JSON output written to: {written_path}[/blue]")

        # --- Now print Run Summary based on (possibly overwritten) result ---
        total_ms = result.timings_ms.get("total_ms") if result.timings_ms else None

        console.print(
            f"\n[bold]Run Summary[/bold]\n"
            f"- request_id: {result.request_id}\n"
            f"- success: {result.success}\n"
            f"- total_ms: {total_ms}\n"
        )

        if not result.success and result.error:
            console.print(
                "[bold red]Failure Details[/bold red]\n"
                f"- error.type: {result.error.type}\n"
                f"- error.message: {result.error.message}\n"
            )
            if result.fallback:
                console.print("[bold]Fallback[/bold]")
                for item in result.fallback:
                    console.print(f"- {item}")

        # Display results
        if result.success:
            console.print("\n[green]✅ Task completed![/green]")
        else:
            console.print("\n[red]❌ Task failed![/red]")
        
        console.print(f"Changes: {len(result.changes)} files modified")


@app.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(f"[bold]Vibe CLI Sandbox[/bold] version {__version__}")


if __name__ == "__main__":
    app()
