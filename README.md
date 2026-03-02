# aib — AI in Bash

AI-powered shell command helper. Describe what you want to do in plain language, pick a command from the interactive menu, and it appears ready-to-run in your terminal.

```
$ aib "find all PDFs modified in the last 7 days"

  Lists PDF files in subdirectories filtered by modification date

  > find . -name "*.pdf" -mtime -7
    find . -name "*.pdf" -newer $(date -d "7 days ago" +%Y-%m-%d)
    fd --extension pdf --changed-within 7d

[Enter to run]
```

The selected command is injected directly into your shell's readline buffer — no copy-paste required.

---

## Installation

### Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) or `pipx`
- [`claude` CLI](https://claude.ai/claude-code) (Claude Max Plan required)

### Install

```bash
# With pipx (recommended)
pipx install aib

# Or with uv
uv tool install aib
```

### Shell Integration

Add the `aib` shell function to your shell config:

```bash
# bash
_aib init >> ~/.bashrc && source ~/.bashrc

# zsh
_aib init --shell zsh >> ~/.zshrc && source ~/.zshrc

# fish
_aib init --shell fish >> ~/.config/fish/config.fish
```

Now use `aib` (not `_aib`) to get readline injection.

---

## Usage

```bash
aib "list files by size, largest first"
aib "kill process on port 8080"
aib "find and delete node_modules directories"
aib "show disk usage of each subdirectory"
aib "compress a directory to tar.gz"
```

### Direct output (no readline injection)

```bash
_aib "your query"
```

---

## How It Works

1. `aib "query"` calls `_aib "query"` and captures its stdout
2. `_aib` sends the query to `claude -p` and parses the response
3. An interactive picker displays the suggested commands
4. The selected command is printed to stdout
5. The `aib` shell function injects it into `READLINE_LINE` (bash) or `print -z` (zsh)

No API key required — uses your existing `claude` CLI session.

---

## Backends

| Backend | Status | Notes |
|---|---|---|
| Claude (`claude -p`) | Available | Requires Claude Code CLI + Max Plan |
| Codex | Planned | |
| Gemini CLI | Planned | |

---

## Configuration

Config file: `~/.config/aib/config.toml`

```toml
backend = "claude"
language = "en"
max_results = 5
timeout = 30
```

---

## Contributing

Issues and PRs welcome. See [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) for the spec.
