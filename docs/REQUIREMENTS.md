# aib Requirements Specification

## Functional Requirements

| ID | Requirement | Status |
|---|---|---|
| FR-001 | Accept a natural language query as CLI argument | ✅ v0.1 |
| FR-002 | Call an AI backend to generate shell command suggestions | ✅ v0.1 |
| FR-003 | Display 3–5 command suggestions in an interactive picker | ✅ v0.1 |
| FR-004 | Print the selected command to stdout | ✅ v0.1 |
| FR-005 | Inject selected command into shell readline buffer | ✅ v0.1 (via shell function) |
| FR-006 | Support bash, zsh, and fish shell integration | ✅ v0.1 |
| FR-007 | Provide `_aib init` to generate shell integration code | ✅ v0.1 |
| FR-008 | Read/write config from `~/.config/aib/config.toml` | ✅ v0.1 |
| FR-009 | Handle AI backend errors gracefully with clear messages | ✅ v0.1 |
| FR-010 | Exit with code 130 on user cancellation (Ctrl+C) | ✅ v0.1 |

## Non-Functional Requirements

### Performance
- AI response should complete within 30 seconds (configurable timeout)
- Picker must be responsive with no noticeable lag

### Portability
- Python 3.10+ on Linux and macOS
- No external binary dependencies beyond `claude` CLI
- Works in any terminal that supports ANSI escape codes

### Usability
- Zero configuration required for first use
- Shell integration installable in a single command
- Picker navigable with arrow keys and Enter

## User Stories

### US-001: Quick Command Lookup
As a developer, I want to describe what I need in plain English so that I don't have to remember exact command syntax.

### US-002: Readline Injection
As a shell user, I want the selected command to appear at my prompt so that I can review and optionally edit it before running.

### US-003: Multiple Options
As a user, I want to see several command alternatives so that I can pick the one that best fits my needs.

### US-004: Easy Setup
As a new user, I want a single command to set up shell integration so that I'm productive immediately.

---

## Backend Interface Specification

```python
class BaseBackend(ABC):
    def query(self, user_input: str) -> BackendResult: ...
    def parse(self, raw: str) -> BackendResult: ...

@dataclass
class BackendResult:
    explanation: str    # One-sentence description
    commands: list[str] # 3–5 shell commands
    raw: str           # Raw AI response for debugging
```

### Expected AI Response Format

```
EXPLANATION: <one sentence>
COMMANDS:
<command 1>
<command 2>
<command 3>
```

---

## Shell Integration Specification

### Bash
```bash
aib() {
  local cmd
  cmd=$(_aib "$@") || return $?
  if [[ -n "$cmd" ]]; then
    READLINE_LINE="$cmd"
    READLINE_POINT=${#cmd}
  fi
}
```

### Zsh
```zsh
aib() {
  local cmd
  cmd=$(_aib "$@") || return $?
  [[ -n "$cmd" ]] && print -z "$cmd"
}
```

### Fish
```fish
function aib
  set cmd (_aib $argv) || return $status
  if test -n "$cmd"
    commandline "$cmd"
  end
end
```

---

## Out of Scope (v1)

- Multi-turn conversation / command refinement
- Context awareness (current directory, git status, installed tools)
- Command history / favorites
- GUI or TUI beyond the picker
- Windows support
- Non-English queries (UI is English; commands work cross-platform)

---

## Future Roadmap

### v0.2
- Context awareness: pass `pwd`, recent command history, OS info to the prompt
- Command history: remember and re-suggest previously used commands

### v0.3
- Gemini CLI backend
- Codex backend

### v1.0
- Plugin system for custom backends
- `aib config` interactive configuration wizard
- Shell completion for subcommands
