"""Abstract base class for aib backends."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class BackendError(Exception):
    """Base exception for backend errors."""


class BackendNotFoundError(BackendError):
    """The backend CLI tool is not installed."""


class BackendTimeoutError(BackendError):
    """The backend timed out."""


@dataclass
class BackendResult:
    """Result from a backend query."""
    explanation: str
    commands: list[str]
    raw: str = ""

    def is_valid(self) -> bool:
        return bool(self.explanation and self.commands)


class BaseBackend(ABC):
    """Abstract base class for AI backends."""

    @abstractmethod
    def query(self, user_input: str) -> BackendResult:
        """Query the backend with a user prompt and return parsed results."""
        ...

    def parse(self, raw: str) -> BackendResult:
        """Parse the structured backend response into a BackendResult."""
        explanation = ""
        commands: list[str] = []
        in_commands = False

        for line in raw.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("EXPLANATION:"):
                explanation = line.removeprefix("EXPLANATION:").strip()
            elif line == "COMMANDS:":
                in_commands = True
            elif in_commands and line:
                commands.append(line)

        return BackendResult(explanation=explanation, commands=commands, raw=raw)
