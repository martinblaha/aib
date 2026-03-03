"""Claude CLI backend for aib."""

import subprocess

from aib.backend.base import (
    BackendError,
    BackendNotFoundError,
    BackendResult,
    BackendTimeoutError,
    BaseBackend,
)
from aib.prompt import QUERY_TEMPLATE


class ClaudeBackend(BaseBackend):
    """Backend that calls `claude -p` as a subprocess."""

    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout

    def query(self, user_input: str) -> BackendResult:
        prompt = QUERY_TEMPLATE.format(query=user_input)
        try:
            result = subprocess.run(
                ["claude", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
        except FileNotFoundError:
            raise BackendNotFoundError(
                "'claude' CLI not found. Install it with: npm install -g @anthropic-ai/claude-code"
            )
        except subprocess.TimeoutExpired:
            raise BackendTimeoutError(
                f"Claude timed out after {self.timeout}s."
            )

        if result.returncode != 0:
            raise BackendError(f"claude exited with error: {result.stderr.strip()}")

        return self.parse(result.stdout)
