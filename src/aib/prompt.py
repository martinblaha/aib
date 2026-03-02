"""AI prompt templates for aib."""

SYSTEM_PROMPT = "You are a shell command expert. Provide practical, commonly-used commands."

QUERY_TEMPLATE = """The user needs a shell command for this task: {query}

Reply in EXACTLY this format (nothing else):
EXPLANATION: <one sentence describing what the commands do>
COMMANDS:
<command 1>
<command 2>
<command 3>

Rules:
- Provide 3-5 commands (most common/simple first)
- Linux/macOS compatible
- No per-command explanations, just the commands
- No markdown, no code blocks, plain text only
"""
