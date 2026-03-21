"""Tests for CLI functionality."""
import pytest
from typer.testing import CliRunner
from vibe_cli_sandbox.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Vibe CLI Sandbox" in result.stdout
