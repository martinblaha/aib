"""Unit tests for CLI entry points."""

from click.testing import CliRunner

from aib.cli import main


runner = CliRunner()


def test_help():
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "AI-powered shell command helper" in result.output


def test_version():
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_no_args_shows_help():
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Usage" in result.output


def test_init_bash(monkeypatch):
    monkeypatch.setenv("SHELL", "/bin/bash")
    result = runner.invoke(main, ["init"])
    assert result.exit_code == 0
    assert "bind -x" in result.output


def test_init_zsh():
    result = runner.invoke(main, ["init", "--shell", "zsh"])
    assert result.exit_code == 0
    assert "print -z" in result.output


def test_init_fish():
    result = runner.invoke(main, ["init", "--shell", "fish"])
    assert result.exit_code == 0
    assert "commandline" in result.output
