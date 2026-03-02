"""Interactive command picker using questionary."""

import questionary
from rich.console import Console

console = Console(stderr=True)

CUSTOM_STYLE = questionary.Style([
    ("qmark", "fg:#5f87ff bold"),
    ("question", "bold"),
    ("answer", "fg:#5fffaf bold"),
    ("pointer", "fg:#5f87ff bold"),
    ("highlighted", "fg:#5f87ff bold"),
    ("selected", "fg:#5fffaf"),
    ("separator", "fg:#6c6c6c"),
    ("instruction", "fg:#6c6c6c"),
])


def pick_command(explanation: str, commands: list[str]) -> str | None:
    """Show an interactive picker and return the selected command, or None if aborted."""
    console.print(f"\n  [dim]{explanation}[/dim]\n")
    try:
        from prompt_toolkit.application.current import create_app_session
        from prompt_toolkit.output import create_output

        # stdout is captured by shell command substitution $(_aib ...).
        # Set up an AppSession with /dev/tty output BEFORE questionary builds
        # the Application+Renderer, so the Renderer uses the TTY from the start.
        with create_app_session(output=create_output(always_prefer_tty=True)):
            selected = questionary.select(
                "Select command:",
                choices=commands,
                style=CUSTOM_STYLE,
                use_shortcuts=False,
            ).ask()
    except (KeyboardInterrupt, EOFError):
        return None
    return selected
