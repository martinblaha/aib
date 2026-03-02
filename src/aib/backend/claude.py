"""Claude CLI backend for aib."""

import subprocess
import sys

from aib.backend.base import BackendResult, BaseBackend
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
            print(
                "Error: 'claude' CLI not found. Install it with: npm install -g @anthropic-ai/claude-code",
                file=sys.stderr,
            )
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print(f"Error: Claude timed out after {self.timeout}s.", file=sys.stderr)
            sys.exit(1)

        if result.returncode != 0:
            print(f"Error from claude: {result.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

        return self.parse(result.stdout)
