"""Click CLI entry points for aib."""

import os
import sys
from typing import Any

import click
from rich.console import Console

from aib import __version__
from aib.backend.claude import ClaudeBackend
from aib import config as cfg
from aib.picker import pick_command
from aib.shell import get_integration

err_console = Console(stderr=True)


class DefaultGroup(click.Group):
    """A click Group that routes unrecognized commands to a default command."""

    def resolve_command(
        self, ctx: click.Context, args: list[str]
    ) -> tuple[str, click.Command, list[str]]:
        # If the first arg matches a known command, use normal resolution.
        if args and args[0] in self.commands:
            return super().resolve_command(ctx, args)
        # Otherwise treat all args as a query for the 'ask' command.
        return "ask", self.commands["ask"], args


@click.group(
    cls=DefaultGroup,
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(__version__, prog_name="_aib")
@click.pass_context
def main(ctx: click.Context) -> None:
    """AI-powered shell command helper.

    Usage:

      _aib "find all PDF files modified in the last 7 days"

      _aib "kill process on port 8080"

    Shell integration (readline injection):

      _aib init >> ~/.bashrc && source ~/.bashrc
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command(name="ask", context_settings={"ignore_unknown_options": True})
@click.argument("query", nargs=-1, required=True)
def ask_cmd(query: tuple[str, ...]) -> None:
    """Ask for a shell command suggestion."""
    run_query(" ".join(query))


@main.command(name="init")
@click.option("--shell", default=None, help="Shell type: bash, zsh, or fish")
def init_cmd(shell: str | None) -> None:
    """Print shell integration code to stdout.

    Usage: _aib init >> ~/.bashrc && source ~/.bashrc
    """
    if shell is None:
        shell = os.environ.get("SHELL", "bash")

    click.echo(get_integration(shell))

    err_console.print(
        "\n[green]Shell integration printed.[/green] "
        "To install, run:\n\n"
        "  [bold]_aib init >> ~/.bashrc && source ~/.bashrc[/bold]\n\n"
        "Then use [bold]aib[/bold] (not [bold]_aib[/bold]) to get readline injection."
    )


def run_query(user_input: str) -> None:
    """Core query flow: call backend, show picker, print result."""
    config = cfg.load()
    backend = ClaudeBackend(timeout=config["timeout"])

    err_console.print(f"  [dim]Asking Claude about:[/dim] [bold]{user_input}[/bold]")

    result = backend.query(user_input)

    if not result.is_valid():
        err_console.print("[red]Error:[/red] Could not parse response from Claude.")
        err_console.print("[dim]Raw response:[/dim]")
        err_console.print(result.raw)
        sys.exit(1)

    commands = result.commands[: config["max_results"]]
    selected = pick_command(result.explanation, commands)

    if selected is None:
        sys.exit(130)  # Interrupted

    # Print to stdout — the shell function captures this and injects into readline
    print(selected)
